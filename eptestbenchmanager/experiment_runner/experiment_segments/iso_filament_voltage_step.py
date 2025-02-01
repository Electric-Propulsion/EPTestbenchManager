import logging
from . import IsoFilamentBase
from numpy import linspace
import time

logger = logging.getLogger(__name__)


class IsoFilamentVoltageStep(IsoFilamentBase):

    def configure(self, config: dict):
        super().configure(config)
        self.min_filament_voltage = config["min_filament_voltage"]
        self.max_filament_voltage = config["max_filament_voltage"]
        self.num_steps = config["num_steps"]
        self.filament_current_limit_value = config["filament_current_limit"]
        self.bias_voltage_setpoint_value = config["bias_voltage"]
        self.bias_current_limit_value = config["bias_current_limit"]
        self.step_delay = config["step_delay"]

    def run(self) -> None:
        self.filament_voltage_setpoint.command(self.min_filament_voltage)
        self.filament_current_limit.command(self.filament_current_limit_value)
        self.bias_voltage_setpoint.command(self.bias_voltage_setpoint_value)
        self.bias_current_limit.command(self.bias_current_limit_value)
        self.bias_output.command(True)
        self.filament_output.command(True)

        voltages = [
            float(voltage)
            for voltage in list(
                linspace(
                    self.min_filament_voltage, self.max_filament_voltage, self.num_steps
                )
            )
        ]

        for voltage in voltages:
            logger.debug("%s: Setting Voltage to %s", self.name, voltage)
            self.filament_voltage_setpoint.command(float(voltage))
            time.sleep(self.step_delay)

        self.filament_output.command(False)
        self.bias_output.command(False)

    def generate_report(self):
        pass
