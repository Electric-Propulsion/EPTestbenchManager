from operator import ge
from . import ExperimentSegment, ThresholdLastNValues, Timeout, AbortingSegmentFailure
import time


class Pumpdown(ExperimentSegment):

    def configure(self, config: dict):
        self.setpoint_mbar = config["setpoint_mbar"]
        self.timeout_time_minutes = config["timeout"]["minutes"]
        self.timeout_action = config["timeout"]["action"]
        self.time_resolution_s = config["time_resolution_s"]
        self.comparison_operator = ge
        self.chamber_pressure = self._testbench_manager.connection_manager.vacuum_chamber_pressure

        self.data = {
            "metadata": {
                "uid": self.uid,
                "start_time": None,
                "end_time": None,
            },
            "pressure": {
                "header": ["time_s", "value_mbar"],
                "data": []
            },
            "termination":{
                "reason": None
            }
        }

    def run(self) -> None:
        with Timeout(Timeout.from_minutes(self.timeout_time_minutes)) as timeout:
            pressure = self.chamber_pressure.value
            threshold = ThresholdLastNValues(20, pressure, self.comparison_operator, float(self.setpoint_mbar))
            self.data["metadata"]["start_time"] = time.time()
            while(threshold.update_evaluate(pressure)):
                if timeout.expired:
                    # We've timed out
                    self.data["termination"]["reason"] = "timeout"
                    self.data["metadata"]["end_time"] = time.time()
                    print(self.data)

                    if(self.timeout_action != "continue"):
                        raise AbortingSegmentFailure(f"{self.uid} segment failed, aborting the experiment. (Reason: {self.data["termination"]["reason"]}")
                    return
                
                next_loop_time = time.perf_counter() + self.time_resolution_s
                
                pressure = self.chamber_pressure.value

                self.data["pressure"]["data"].append([time.time(), pressure])
                
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
        print(self.data)
        return


    def generate_report(self):
        pass
