import logging
from . import ExperimentSegment
from numpy import linspace
import time

logger = logging.getLogger(__name__)


class Step(ExperimentSegment):

    def configure(self, config: dict):
        self.min = config["start"]
        self.max = config["stop"]
        self.num_steps = config["num_steps"]
        self.step_delay = config["step_delay"]
        self.reset = config.get("reset", False)
        self.commanded_vinstrument_setpoint = self._testbench_manager.connection_manager.virtual_instruments[config["commanded_vinstrument_setpoint"]]
        output_name = config.get("commanded_vinstrument_output", None)
        if output_name is not None:
            self.commanded_vinstrument_output = self._testbench_manager.connection_manager.virtual_instruments[output_name]
        else:
            self.commanded_vinstrument_output = None

    def run(self) -> None:
        self.commanded_vinstrument_setpoint.command(self.min)
        if self.commanded_vinstrument_output is not None:
            self.commanded_vinstrument_output.command(True)

        values = [
            float(value)
            for value in list(
                linspace(
                    self.min, self.max, self.num_steps
                )
            )
        ]

        for value in self.interruptable(values):
            logger.debug("%s: Setting to %s", self.name, value)
            self.commanded_vinstrument_setpoint.command(float(value))
            self.interruptable_sleep(self.step_delay)

        if self.commanded_vinstrument_output is not None and self.reset:
            self.commanded_vinstrument_output.command(False)

    def generate_report(self):
        pass
