import time
from . import ExperimentSegment


class Hold(ExperimentSegment):


    def configure(self, config: dict):
        self.setpoint = config["setpoint"]
        self.hold_s = config["hold_s"]
        
        self.commanded_vinstrument_setpoint = self._testbench_manager.connection_manager.virtual_instruments[config["commanded_vinstrument_setpoint"]]
        
        output_name = config.get("commanded_vinstrument_output", None)
        if output_name is not None:
            self.commanded_vinstrument_output = self._testbench_manager.connection_manager.virtual_instruments[output_name]
        else:
            self.commanded_vinstrument_output = None
        
        value_name = config.get("value_vinstrument", None)
        if value_name is not None:
            self.value_vinstrument = self._testbench_manager.connection_manager.virtual_instruments[value_name]
        else:
            self.value_vinstrument = None
        
        self.reset = config.get("reset", False) and self.value_vinstrument is not None
        # will first try to reset
        # then will try to turn off output
        # then will just leave


    def run(self) -> None:
        if self.reset:
            reset_value = self.value_vinstrument.value()
        
        self.commanded_vinstrument_setpoint.command(True)
        
        if self.commanded_vinstrument_output is not None:
            self.commanded_vinstrument_output.command(True)
        
        self.interruptable_sleep(self.hold_s)
        
        if self.reset:
            self.commanded_vinstrument_setpoint.command(reset_value)
        elif self.commanded_vinstrument_output is not None:
            self.commanded_vinstrument_output.command(False)
        

    def generate_report(self):
        pass
