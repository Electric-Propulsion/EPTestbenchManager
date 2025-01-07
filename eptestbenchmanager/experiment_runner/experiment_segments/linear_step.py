from . import ExperimentSegment
from .. import ExperimentFactory

class LinearStep(ExperimentSegment):
    """Represents a segment that steps through a value, and executes another step at each value"""

    def configure(self, config: dict):
        self.min_value = config["min_value"]
        self.max_value = config["max_value"]
        self.step_size = config["step_size"]
        self.segment = config["segment"]
        self.segment_constants = config["constants"]
        self.segment_variable = config["variable"]
        self.segment_class = ExperimentFactory.get_class(self.segment)

        self.values = range(self.min_value, self.max_value, self.step_size)
        self.segments = []
        for value in self.values:
            name = f"{self.name} Step: {value}"
            uid = f"{self.name}_step_{value}"
            config = self.segment_constants
            config[self.segment_variable] = value
            self.segments.append(
                self.segment_class(uid, name, config, self._testbench_manager)
            )

    def run(self):
        for segment in self.segments:
            segment.run()
        