from operator import ge
import time
from . import ExperimentSegment, ThresholdLastNValues, Timeout, AbortingSegmentFailure


class Pumpdown(ExperimentSegment):
    """Represents a pumpdown segment in an experiment.

    This class handles the configuration and execution of a pumpdown segment, monitoring the chamber
    pressure and ensuring it reaches a specified setpoint within a given timeout period.
    """

    def configure(self, config: dict):
        """Configures the pumpdown segment with the provided settings.

        Args:
            config (dict): Configuration dictionary containing setpoint, timeout, and other
            settings.
        """
        self.setpoint_mbar = config["setpoint_mbar"]
        self.timeout_time_minutes = config["timeout"]["minutes"]
        self.timeout_action = config["timeout"]["action"]
        self.time_resolution_s = config["time_resolution_s"]
        self.comparison_operator = ge
        self.chamber_pressure = (
            self._testbench_manager.connection_manager.vacuum_chamber_pressure
        )

        self.data = {
            "metadata": {
                "uid": self.uid,
                "start_time": None,
                "end_time": None,
            },
            "pressure": {"header": ["time_s", "value_mbar"], "data": []},
            "termination": {"reason": None},
        }

    def run(self) -> None:
        """Executes the pumpdown segment.

        Monitors the chamber pressure and ensures it reaches the setpoint within the timeout period.
        """
        with Timeout(Timeout.from_minutes(self.timeout_time_minutes)) as timeout:
            pressure = self.chamber_pressure.value
            threshold = ThresholdLastNValues(
                20, pressure, self.comparison_operator, float(self.setpoint_mbar)
            )
            self.data["metadata"]["start_time"] = time.time()
            while threshold.update_evaluate(pressure):
                if timeout.expired:
                    # We've timed out
                    self.data["termination"]["reason"] = "timeout"
                    self.data["metadata"]["end_time"] = time.time()

                    if self.timeout_action != "continue":
                        raise AbortingSegmentFailure(
                            f"{self.uid} segment failed, aborting the experiment. (Reason: {self.data['termination']['reason']}"  # pylint: disable=line-too-long
                        )
                    return

                next_loop_time = time.perf_counter() + self.time_resolution_s

                pressure = self.chamber_pressure.value

                self.data["pressure"]["data"].append(
                    [time.time(), pressure]
                )  # TODO: Remove; this should be handled by recordings.

                sleep_time = next_loop_time - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    # We missed the next read
                    # TODO: Log a warning
                    pass

        # We're at the specified pressure
        self.data["termination"]["reason"] = "success"
        self.data["metadata"]["end_time"] = time.time()
        return

    def generate_report(self):
        """Generates a report for the pumpdown segment.

        This method is a placeholder and should be implemented to generate a detailed report.
        """
