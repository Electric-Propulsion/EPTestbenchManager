import logging
from threading import Thread, Lock, Event
import time
import datetime
from io import StringIO
from typing import TYPE_CHECKING
from eptestbenchmanager.chat.alert_manager import AlertSeverity
from .experiment_segments.experiment_segment import (
    ExperimentSegment,
    AbortingSegmentFailure,
)

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager

logger = logging.getLogger(__name__)


class Experiment:
    """Represents an experiment consisting of multiple segments.

    Attributes:
        uid (str): Unique identifier for the experiment.
        name (str): Name of the experiment.
        description (str): Description of the experiment.
        segments (list[ExperimentSegment]): List of segments in the experiment.
        current_segment_id (int): ID of the current segment being executed.
        _experiment_lock (Lock): Lock to ensure exclusive access to the experiment.
        operator (str): Operator running the experiment.
        _testbench_manager (TestbenchManager): Global TestbenchManager object.
        run_id (str): Identifier for the current run of the experiment.
    """

    def __init__(
        self,
        uid: str,
        name: str,
        description: str,
        segments: list[ExperimentSegment],
        experiment_lock: Lock,
        testbench_manager: "TestbenchManager",
    ):
        """Initializes the Experiment with the given parameters.

        Args:
            uid (str): Unique identifier for the experiment.
            name (str): Name of the experiment.
            description (str): Description of the experiment.
            segments (list[ExperimentSegment]): List of segments in the experiment.
            experiment_lock (Lock): Lock to ensure exclusive access to the experiment.
            testbench_manager (TestbenchManager): Global TestbenchManager object.
        """
        self.uid: str = uid
        self.name: str = name
        self.description: str = description
        self.segments: list[ExperimentSegment] = segments
        self.current_segment_id = -1
        self._experiment_lock: Lock = experiment_lock
        self.operator: str = None
        self._testbench_manager = testbench_manager
        self.run_id: str = None  # Not defined until the first run
        for segment in self.segments:  # Inject the experiment into the segments
            segment.inject_experiment(self)
        self._runner_thread: Thread = None
        self.start_time: float = None
        self.abort = Event()
        self.abort.clear()

    def run(self, operator: str) -> None:
        """Starts the experiment by creating and starting a new thread.

        Args:
            operator (str): Operator running the experiment.
        """
        self.run_id = f"{self.uid}_{time.strftime('%Y%m%d_%H%M%S')}"
        self.operator = operator
        self._runner_thread = Thread(
            target=self.run_segments, name=f"{self.uid} Runner Thread", daemon=True
        )
        self.abort.clear()
        self._runner_thread.start()

    def request_abort(self) -> None:
        """Requests the experiment to abort."""
        self.abort.set()

    def run_segments(self) -> None:
        """Runs all segments of the experiment sequentially."""
        self.start_time = time.perf_counter()

        self._testbench_manager.alert_manager.send_alert(
            f"Starting experiment **{self.name}**. ({len(self.segments)} segments)\nRun ID: {self.run_id}",  # pylint: disable=line-too-long
            severity=AlertSeverity.INFO,
            target=self.operator,
        )
        try:
            self.current_segment_id = -1

            for segment in self.segments:
                segment_start_time = time.perf_counter()
                self.current_segment_id += 1

                # Update the appropriate virtual instruments
                self._testbench_manager.connection_manager.virtual_instruments[
                    "experiment_current_segment_id"
                ].set_value(self.current_segment_id)
                self._testbench_manager.connection_manager.virtual_instruments[
                    "experiment_current_segment_uid"
                ].set_value(segment.uid)
                self._testbench_manager.connection_manager.virtual_instruments[
                    "experiment_current_segment_name"
                ].set_value(segment.name)

                try:
                    self._testbench_manager.alert_manager.send_alert(
                        (
                            f"Experiment **{self.name}** is running segment "
                            f"**{self.segments[self.current_segment_id].uid}**. Elapsed time: "
                            f"{datetime.timedelta(seconds=segment_start_time - self.start_time)}. "
                            f"({self.current_segment_id+1}/{len(self.segments)})"
                        ),
                        severity=AlertSeverity.INFO,
                        target=self.operator,
                    )
                    if self.abort.is_set():
                        raise AbortingSegmentFailure("Manual abort requested.")
                    segment.prerun()
                    segment.run()
                    segment.postrun()

                except AbortingSegmentFailure as e:
                    # TODO: indicate somehow that we're aborting
                    logger.error("Aborting segment %s: %s", segment.uid, e)

                    self._testbench_manager.alert_manager.send_alert(
                        (
                            f"Experiment **{self.name}** has aborted at segment "
                            f"**{self.segments[self.current_segment_id].uid}**. Elapsed time: "
                            f"{datetime.timedelta(seconds=time.perf_counter()- self.start_time)} "
                            f"(reason: {e})"
                        ),
                        severity=AlertSeverity.INFO,
                        target=self.operator,
                    )

                    return

            # Add one more to indicate we're finished
            self.current_segment_id += 1

        finally:
            # Allow other experiments to run
            self._experiment_lock.release()

            end_time = time.perf_counter()

            log_archive_path = self._testbench_manager.report_manager.create_archive(
                self.run_id, self.run_id
            )

            self._testbench_manager.alert_manager.send_alert(
                (
                    f"Experiment **{self.name}** has completed. Completed in "
                    f"{datetime.timedelta(seconds=end_time - self.start_time)}."
                ),
                severity=AlertSeverity.INFO,
                target=self.operator,
            )

            self._testbench_manager.alert_manager.send_file(
                file_path=log_archive_path,
                severity=AlertSeverity.INFO,
            )

            # Reset the operator
            self.operator = None

    def generate_report(self) -> StringIO:
        """Generates a report for the experiment.

        Returns:
            StringIO: The generated report.
        """
        for segment in self.segments:
            segment.generate_report()
        # TODO: return the report

    def get_current_segment_uid(self) -> str:
        """Gets the UID of the current segment.

        Returns:
            str: UID of the current segment, or "no segment" if index is out of range.
        """
        try:
            return self.segments[self.current_segment_id].uid
        except IndexError:
            return "no segment"

    @property
    def rules(self):
        """Gets the rules of the active segment.

        Returns:
            None
        """
        # TODO: need to get just the rule from the active segment?
