from . import IsoFilamentBase
from numpy import linspace
import time

class IsoFilamentVoltageStep(IsoFilamentBase):

    def configure(self, config: dict):
        super().configure(config)
        self.min_filament_voltage = config["min_filament_voltage"]
        self.max_filament_voltage = config["max_filament_voltage"]
        self.num_steps = config["num_steps"]
        self.filament_current_limit_setpoint = config["filament_current_limit"]
        self.bias_voltage_setpoint = config["bias_voltage"]
        self.bias_current_limit_setpoint = config["bias_current_limit"]
        self.step_delay = config["step_delay"]

    def run(self) -> None:
        self.filament_voltage.command(self.min_filament_voltage)
        self.filament_current_limit.command(self.filament_current_limit_setpoint)
        self.bias_voltage.command(self.bias_voltage_setpoint)
        self.bias_current_limit.command(self.bias_current_limit_setpoint)
        self.bias_output.command(True)
        self.filament_output.command(True)

        voltages = [float(voltage) for voltage in list(linspace(self.min_filament_voltage, self.max_filament_voltage, self.num_steps))]

        for voltage in voltages:
            print(f"{self.name}: Setting Voltage to {voltage}")
            self.filament_voltage.command(float(voltage))
            time.sleep(self.step_delay)

        self.filament_output.command(False)
        self.bias_output.command(False)

    def generate_report(self):
        pass

    