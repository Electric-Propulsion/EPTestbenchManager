import time
from . import IsoFilamentBase


class IsoFilamentHold(IsoFilamentBase):
    """
    Represents a segment that holds an isotropic filament at some values for some time
    """

    def configure(self, config: dict):
        super().configure(config)
        self.filament_voltage_setpoint_value = config["filament_voltage"]
        self.filament_current_limit_value = config["filament_current_limit"]
        self.bias_voltage_setpoint_value = config["bias_voltage"]
        self.bias_current_limit_value = config["bias_current_limit"]
        self.hold_s = config["hold_s"]

    def run(self) -> None:
        self.bias_current_limit.command(self.bias_current_limit_value)
        self.bias_voltage_setpoint.command(self.bias_voltage_setpoint_value)
        self.filament_current_limit.command(self.filament_current_limit_value)
        self.filament_voltage_setpoint.command(self.filament_voltage_setpoint_value)
        self.filament_output.command(True)
        self.bias_output.command(True)
        time.sleep(self.hold_s)
        self.filament_output.command(False)
        self.bias_output.command(False)

    def generate_report(self):
        pass
