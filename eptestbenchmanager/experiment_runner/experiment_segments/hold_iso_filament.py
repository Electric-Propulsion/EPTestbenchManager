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
        self.filament_output = self._testbench_manager.connection_manager.filament_current_output
        
        self.bias_voltage = self._testbench_manager.connection_manager.bias_voltage
        self.bias_current_limit = self._testbench_manager.connection_manager.bias_current_limit
        self.bias_output = self._testbench_manager.connection_manager.bias_current_output

        self.data = {} #TODO: remove self.data at some point? or fix

    def run(self) -> None:
        self.bias_output.command(True)
        self.filament_output.command(True)
        self.bias_current_limit.command(self.bias_current_limit_setpoint)
        self.bias_voltage.command(self.bias_voltage_setpoint)
        self.filament_current_limit.command(self.filament_current_limit_setpoint)
        self.filament_voltage.command(self.filament_voltage_setpoint)
        self.filament_voltage.command
        time.sleep(self.hold_s)
        self.bias_output.command(False)
        self.filament_output.command(False)

    def generate_report(self):
        pass


        
