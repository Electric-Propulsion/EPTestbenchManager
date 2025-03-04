from . import ExperimentSegment


class Set(ExperimentSegment):


    def configure(self, config: dict):
        self.setpoint = config["setpoint"]
        
        self.commanded_vinstrument_setpoint = self._testbench_manager.connection_manager.virtual_instruments[config["commanded_vinstrument_setpoint"]]
        
        output_name = config.get("commanded_vinstrument_output", None)
        self.enable = config.get("enable", True)
        if output_name is not None:
            self.commanded_vinstrument_output = self._testbench_manager.connection_manager.virtual_instruments[output_name]
        else:
            self.commanded_vinstrument_output = None

    def run(self) -> None:
        
        self.commanded_vinstrument_setpoint.command(True)
        
        if self.commanded_vinstrument_output is not None:
            self.commanded_vinstrument_output.command(self.enable)
        

    def generate_report(self):
        pass
