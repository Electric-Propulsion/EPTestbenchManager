from threading import Thread, Lock
import time, datetime
from eptestbenchmanager.chat.alert_manager import AlertSeverity
from .experiment_segments.experiment_segment import (
    ExperimentSegment,
    AbortingSegmentFailure,
)
from io import StringIO
import os
from pathlib import Path
import zipfile


class Experiment:

    def __init__(
        self,
        uid: str,
        name: str,
        description: str,
        segments: list[ExperimentSegment],
        experiment_lock: Lock,
        testbench_manager: "TestbenchManager",
    ):
        self.uid: str = uid
        self.name: str = name
        self.description: str = description
        self.segments: list[ExperimentSegment] = segments
        self.current_segment_id = -1
        self._experiment_lock: Lock() = experiment_lock
        self.operator: str = None
        self._testbench_manager = testbench_manager
        self.run_id: str = None # Not defined until the first run
        for segment in self.segments: # Inject the experiment into the segments
            segment.inject_experiment(self)

    def run(self, operator: str) -> None:
        self.run_id = f"{self.uid}_{time.strftime('%Y%m%d_%H%M%S')}"
        self.operator = operator
        self._runner_thread = Thread(
            target=self.run_segments, name=f"{self.uid} Runner Thread", daemon=False
        )
        self._runner_thread.start()

    def run_segments(self) -> None:

        self.start_time = time.perf_counter()
        

        self._testbench_manager.alert_manager.send_alert(
            f"Starting experiment **{self.name}**. ({len(self.segments)} segments)\nRun ID: {self.run_id}",
            severity=AlertSeverity.INFO,
            target=self.operator,
        )
        try:

            self.current_segment_id = -1

            for segment in self.segments:

                segment_start_time = time.perf_counter()
                self.current_segment_id += 1


                # Update the appropriate virtual instruments
                self._testbench_manager.connection_manager.virtual_instruments["experiment_current_segment_id"]._set_value(self.current_segment_id)
                self._testbench_manager.connection_manager.virtual_instruments["experiment_current_segment_uid"]._set_value(segment.uid)
                self._testbench_manager.connection_manager.virtual_instruments["experiment_current_segment_name"]._set_value(segment.name)


                try:

                    self._testbench_manager.alert_manager.send_alert(
                        f"Experiment **{self.name}** is running segment **{self.segments[self.current_segment_id].uid}**. Elapsed time: {datetime.timedelta(seconds=segment_start_time - self.start_time)}. ({self.current_segment_id+1}/{len(self.segments)})",
                        severity=AlertSeverity.INFO,
                        target=self.operator,
                    )
                    segment.prerun()
                    segment.run()
                    segment.postrun()


                    print(segment.data)  # TODO: remove this

                except AbortingSegmentFailure as e:

                    # TODO: indicate somehow that we're aborting
                    print("Aborting segment")
                    print(e)
                    print(segment.data)

                    self._testbench_manager.alert_manager.send_alert(
                        f"Experiment **{self.name}** has aborted at segment **{self.segments[self.current_segment_id].uid}**. Elapsed time: {datetime.timedelta(seconds=segment_start_time - self.start_time)}  (reason: {e})",
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

            log_archive_path = self._testbench_manager.report_manager.create_archive(self.run_id, self.run_id)

            self._testbench_manager.alert_manager.send_alert(
                f"Experiment **{self.name}** has completed. Completed in {datetime.timedelta(seconds=end_time - self.start_time)}.",
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
        for segment in self.segments:
            segment.generate_report()
        # TODO: return the report


    def get_current_segment_uid(self) -> str:
        try:
            return self.segments[self.current_segment_id].uid
        except IndexError:
            return "no segment"


    @property
    def rules(self):
        pass  # TODO: need to get just the rule from the active segment?
