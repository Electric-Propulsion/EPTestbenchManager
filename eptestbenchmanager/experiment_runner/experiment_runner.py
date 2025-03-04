import logging
from pathlib import Path
from io import StringIO
from os import path, walk
from threading import Lock, Thread
from typing import TYPE_CHECKING
from .experiment import Experiment
from .experiment_factory import ExperimentFactory

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager

logger = logging.getLogger(__name__)


class ExperimentRunner:
    """Manages and runs experiments for the testbench.

    Attributes:
        _experiments (dict[str, Experiment]): Dictionary of experiments keyed by their UID.
        _testbench_manager (TestbenchManager): Global TestbenchManager object.
        _experiment_lock (Lock): Lock to ensure only one experiment runs at a time.
        _current_experiment_uid (str): UID of the currently running experiment.
    """

    def __init__(
        self, testbench_manager: "TestbenchManager", experiment_config_dir: Path
    ):
        """Initializes the ExperimentRunner with a testbench manager.

        Args:
            testbench_manager (TestbenchManager): Manager for the testbench.
        """
        self._experiments: dict[str, Experiment] = {}
        self._testbench_manager = testbench_manager
        self._experiment_lock = Lock()
        self._current_experiment_uid = None
        self.experiment_config_dir = experiment_config_dir

    def load_experiments(self) -> None:
        for dirpath, _, filenames in walk(self.experiment_config_dir):
            for filename in filenames:
                if filename.endswith(".yaml"):
                    with open(
                        path.join(dirpath, filename), "r", encoding="utf-8"
                    ) as experiment_config_file:
                        try:
                            self.add_experiment(experiment_config_file)
                        except Exception as e:
                            logger.error(
                                f"Error loading experiment {filename}: {e} (Possibly incompatible with current apparatus)"
                            )

    def request_abort_current_experiment(self) -> None:
        """Requests the current experiment
        to be aborted."""
        if self._current_experiment_uid is not None:
            self._experiments[self._current_experiment_uid].request_abort()

    def add_experiment(self, experiment_file: StringIO) -> None:
        """Adds an experiment to the runner.

        Args:
            experiment_file (StringIO): File containing the experiment configuration.
        """
        experiment = ExperimentFactory.create_experiment(
            experiment_file, self._testbench_manager, self._experiment_lock
        )
        self._experiments[experiment.uid] = experiment

    def run_experiment(self, uid: str, operator: str) -> None:
        """Runs the experiment with the given UID.

        Args:
            uid (str): Unique identifier of the experiment.
            operator (str): Name of the operator running the experiment.
        """
        if self._experiment_lock.acquire(blocking=False):
            logger.info("Running experiment %s", uid)
            self._current_experiment_uid = uid
            self._experiments[uid].run(operator)
            Thread(target=self.wait_for_experiment_end).start()

        else:
            logger.warning(
                "Cannot start experiment %s. Experiment %s is already running",
                uid,
                self.get_current_experiment_uid(),
            )

    def wait_for_experiment_end(self) -> None:
        self._experiment_lock.acquire()
        self._current_experiment_uid = None
        self._experiment_lock.release()


    def remove_experiment(self, uid: str) -> None:
        """Removes the experiment with the given UID.

        Args:
            uid (str): Unique identifier of the experiment to remove.
        """
        self._experiments.pop(uid)

    def get_experiment_segments(self, experiment_uid: str) -> list:
        """Gets the segments of the specified experiment.

        Args:
            experiment_uid (str): Unique identifier of the experiment.

        Returns:
            list: List of segments in the experiment.
        """
        return self._experiments[experiment_uid].segments

    def get_experiment_current_segment_uid(self, experiment_uid: str) -> str:
        """Gets the UID of the current segment of the specified experiment.

        Args:
            experiment_uid (str): Unique identifier of the experiment.

        Returns:
            str: UID of the current segment.
        """
        if experiment_uid is not None:
            return self._experiments[experiment_uid].get_current_segment_uid()
        return "No experiment"

    def get_experiment_current_segment_id(self, experiment_uid: str) -> int:
        """Gets the ID of the current segment of the specified experiment.

        Args:
            experiment_uid (str): Unique identifier of the experiment.

        Returns:
            int: ID of the current segment.
        """
        return self._experiments[experiment_uid].current_segment_id

    def get_current_experiment_uid(self) -> str:
        """Gets the UID of the currently running experiment.

        Returns:
            str: UID of the currently running experiment.
        """
        return self._current_experiment_uid

    def get_current_experiment_run_id(self) -> str:
        """Gets the run ID of the currently running experiment.

        Returns:
            str: Run ID of the currently running experiment.
        """
        return self._experiments[self._current_experiment_uid].run_id

    @property
    def experiments(self) -> dict[str, Experiment]:
        """Gets the dictionary of experiments.

        Returns:
            dict[str, Experiment]: Dictionary of experiments.
        """
        return self._experiments.keys()
