from . import ExperimentSegment

class IsoFilamentBase(ExperimentSegment):

    def configure(self, config: dict):

        self.filament_voltage = self._testbench_manager.connection_manager.filament_voltage
        self.filament_current_limit = self._testbench_manager.connection_manager.filament_current_limit
        self.filament_output = self._testbench_manager.connection_manager.filament_output

        self.bias_voltage = self._testbench_manager.connection_manager.bias_voltage
        self.bias_current_limit = self._testbench_manager.connection_manager.bias_current_limit
        self.bias_output = self._testbench_manager.connection_manager.bias_output

        self.data = {} #TODO: remove self.data at some point? or fix