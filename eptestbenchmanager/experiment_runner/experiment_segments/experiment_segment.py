from abc import ABC, abstractmethod
from threading import Thread
from os import path
from typing import TYPE_CHECKING
from eptestbenchmanager.monitor import Rule

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager


class AbortingSegmentFailure(Exception):
    """Exception raised to indicate that the experiment should terminate."""


class ExperimentSegment(ABC):
    """Abstract base class for an experiment segment.

    Attributes:
        uid (str): Unique identifier for the segment.
        name (str): Name of the segment.
        _rules (list[Rule]): List of rules associated with the segment.
        _runner_thread (Thread): Thread for running the segment.
        _testbench_manager (TestbenchManager): Global TestbenchManager object.
        data: Data associated with the segment.
        _recordings (list): List of recordings configurations.
        _segment_view (list): View of the segment.
        experiment: Experiment associated with the segment.
    """

    def __init__(
        self, uid: str, name: str, config: dict, testbench_manager: "TestbenchManager"
    ):
        """Initializes the ExperimentSegment.

        Args:
            uid (str): Unique identifier for the segment.
            name (str): Name of the segment.
            config (dict): Configuration dictionary for the segment.
            testbench_manager (TestbenchManager): Global TestbenchManager object.
        """
        self.uid = uid
        self.name = name
        self._rules: list[Rule] = []
        self._runner_thread: Thread = None
        self._testbench_manager = testbench_manager
        self.data = None
        self.configure(config)
        self._recordings = config["recordings"] if "recordings" in config else []
        self._segment_view = []
        self.experiment = None

    def inject_experiment(self, experiment):
        """Injects the experiment into the segment.

        Args:
            experiment: Experiment to be injected.
        """
        self.experiment = experiment

    @abstractmethod
    def configure(self, config: dict):
        """Configures the segment.

        Args:
            config (dict): Configuration dictionary.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def run(self) -> None:
        """Runs the segment.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Trying to run an abstract class!")

    @abstractmethod
    def generate_report(self):
        """Generates a report for the segment.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError("Trying to generate a report from an abstract class.")

    @property
    def rules(self) -> list[Rule]:
        """Gets the rules associated with the segment.

        Returns:
            list[Rule]: List of rules.
        """
        return self._rules

    def start_recordings(self):
        """Starts the recordings for the segment.

        Raises:
            ValueError: If a virtual instrument is not found in the testbench manager.
        """
        for vinstrument_data in self._recordings:
            vinstrument_id = list(vinstrument_data.keys())[0]
            record_id = self.generate_record_id(
                vinstrument_data[vinstrument_id]["record_id"]
            )
            if (
                vinstrument_id
                not in self._testbench_manager.connection_manager.virtual_instruments
            ):
                raise ValueError(
                    f"Virtual instrument {vinstrument_id} not found in testbench manager."
                )

            vinstrument = (
                self._testbench_manager.connection_manager.virtual_instruments[
                    vinstrument_id
                ]
            )

            if vinstrument.recording_exists(record_id):
                vinstrument.resume_recording(record_id)
            else:
                file_id = self.generate_file_id(record_id)
                record_name = vinstrument_data[vinstrument_id]["record_name"]
                vinstrument.begin_recording(record_id, record_name, file_id=file_id)

    def stop_recordings(self):
        """Stops the recordings for the segment.

        Raises:
            ValueError: If a virtual instrument is not found in the testbench manager.
        """
        for vinstrument_data in self._recordings:
            vinstrument_id = list(vinstrument_data.keys())[0]
            record_id = self.generate_record_id(
                vinstrument_data[vinstrument_id]["record_id"]
            )
            if (
                vinstrument_id
                not in self._testbench_manager.connection_manager.virtual_instruments
            ):
                raise ValueError(
                    f"Virtual instrument {vinstrument_id} not found in testbench manager."
                )

            vinstrument = (
                self._testbench_manager.connection_manager.virtual_instruments[
                    vinstrument_id
                ]
            )
            vinstrument.stop_recording(record_id)

    def prerun(self):
        """Performs pre-run operations for the segment."""
        self.start_recordings()

    def postrun(self):
        """Performs post-run operations for the segment."""
        self.stop_recordings()

    def generate_file_id(self, record_id: str) -> str:  # pylint disable=invalid-name
        """Generates a file ID for the recording.

        Args:
            record_id (str): Record ID.

        Returns:
            str: Generated file ID.
        """
        return path.join(self.experiment.run_id, record_id)

    def generate_record_id(self, record_id: str) -> str:  # pylint disable=invalid-name
        """Generates a record ID for the recording.

        Args:
            record_id (str): Record ID.

        Returns:
            str: Generated record ID.
        """
        return f"{self.experiment.run_id}_{record_id}"
