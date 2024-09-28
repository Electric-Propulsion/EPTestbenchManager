from operator import ge
from . import Pumpdown, Timeout, ThresholdLastNValues, AbortingSegmentFailure
import time


class MeasureLeaks(Pumpdown):

    def configure(self, config: dict):
        config["setpoint_mbar"] = config["end_pressure_mbar"]
        super().configure()
        self.comparison_operator = ge

