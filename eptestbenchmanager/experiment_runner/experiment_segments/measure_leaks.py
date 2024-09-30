from operator import le
from . import Pumpdown, Timeout, ThresholdLastNValues, AbortingSegmentFailure
import time


class MeasureLeaks(Pumpdown):

    def configure(self, config: dict):
        config["setpoint_mbar"] = config["end_pressure_mbar"]
        super().configure(config)
        self.comparison_operator = le
        self.uid = "meas_leaks"

