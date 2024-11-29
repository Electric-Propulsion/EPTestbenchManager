from operator import ge
from . import Pumpdown, Timeout, ThresholdLastNValues, AbortingSegmentFailure
import time


class MeasureLeaks(Pumpdown):

    def configure(self, config: dict):
        config["setpoint_mbar"] = config["end_pressure_mbar"]
        super().configure(config)
        self.comparison_operator = ge
        self.chamber_pressure = self._testbench_manager.connection_manager.vacuum_chamber_pressure



    def run(self) -> None:
        with Timeout(Timeout.from_minutes(self.timeout_time_minutes)) as timeout:
            pressure = self.chamber_pressure.value
            threshold = ThresholdLastNValues(20, pressure, self.comparison_operator, float(self.setpoint_mbar))
            self.data["metadata"]["start_time"] = time.time()
            while(threshold.update_evaluate(pressure)):
                if timeout.expired:

                    if(self.timeout_action != "continue"):
                        raise AbortingSegmentFailure(f"{self.uid} segment failed, aborting the experiment. (Reason: {self.data["termination"]["reason"]}")
                    return
                
                next_loop_time = time.perf_counter() + self.time_resolution_s
                
                pressure = self.chamber_pressure.value

                
                sleep_time = next_loop_time - time.perf_counter()
                if sleep_time > 0:
                    time.sleep(sleep_time)
                else:
                    # We missed the next read
                    # TODO: Log a warning
                    pass

        # We're at the specified pressure

        return

