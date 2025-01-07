from . import ExperimentSegment

class HoldIsoFilament(ExperimentSegment):
    """
    Represents a segment that holds an isotropic filament at some values for some time
    """

    def configure(self, config: dict):
        self.filament_voltage = config["filament_voltage"]
        self.bias_voltage = config["bias_voltage"]
        self.hold_s = config["hold_s"]

        self.data = {}
