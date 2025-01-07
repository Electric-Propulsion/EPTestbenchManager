import time
from . import ExperimentSegment

class HoldIsoFilament(ExperimentSegment):
    """
    Represents a segment that holds an isotropic filament at some values for some time
    """

    def configure(self, config: dict):
        self.filament_voltage_setpoint = config["filament_voltage"]
        self.filament_current_limit_setpoint = config["filament_current_limit"]
        self.bias_voltage_setpoint = config["bias_voltage"]
        self.bias_current_limit_setpoint = config["bias_current_limit"]
        self.hold_s = config["hold_s"]

        self.filament_voltage = self._testbench_manager.connection_manager.filament_voltage
        self.filament_current_limit = self._testbench_manager.connection_manager.filament_current_limit

        self.bias_voltage = self._testbench_manager.connection_manager.bias_voltage
        self.bias_current_limit = self._testbench_manager.connection_manager.bias_current_limit

        self.data = {} #TODO: remove self.data at some point? or fix

    def run(self) -> None:
        self.bias_current_limit.command(self.bias_current_limit_setpoint)
        self.bias_voltage.command(self.bias_voltage_setpoint)
        self.filament_current_limit.command(self.filament_current_limit_setpoint)
        self.filament_voltage.command(self.filament_voltage_setpoint)
        time.sleep(self.hold_s)

    def generate_report(self):
        pass


        
