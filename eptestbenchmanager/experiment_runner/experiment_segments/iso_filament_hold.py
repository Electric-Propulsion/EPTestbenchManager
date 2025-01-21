import time
from . import IsoFilamentBase

class IsoFilamentHold(IsoFilamentBase):
    """
    Represents a segment that holds an isotropic filament at some values for some time
    """

    def configure(self, config: dict):
        super().configure(config)
        self.filament_voltage_setpoint = config["filament_voltage"]
        self.filament_current_limit_setpoint = config["filament_current_limit"]
        self.bias_voltage_setpoint = config["bias_voltage"]
        self.bias_current_limit_setpoint = config["bias_current_limit"]
        self.hold_s = config["hold_s"]

        
    def run(self) -> None:
        self.bias_current_limit.command(self.bias_current_limit_setpoint)
        self.bias_voltage.command(self.bias_voltage_setpoint)
        self.filament_current_limit.command(self.filament_current_limit_setpoint)
        self.filament_voltage.command(self.filament_voltage_setpoint)
        self.filament_output.command(True)
        self.bias_output.command(True)
        time.sleep(self.hold_s)
        self.filament_output.command(False)
        self.bias_output.command(False)

    def generate_report(self):
        pass


        
