from numpy import linspace
from . import ExperimentSegment


class LinearStep(ExperimentSegment):
    """Represents a segment that steps through a value, and executes another step at each value"""

    def configure(self, config: dict):
        # down here to avoid circular imports
        from eptestbenchmanager.experiment_runner import ExperimentFactory

        self.min_value = config["min_value"]
        self.max_value = config["max_value"]
        self.num_steps = config["num_steps"]
        self.segment = config["segment"]
        self.segment_constants = config["constants"]
        self.segment_variable = config["variable"]
        self.segment_class = ExperimentFactory.get_class(self.segment)

        self.values = list(linspace(self.min_value, self.max_value, self.num_steps))
        self.segments = []
        for i, value in enumerate(self.values):
            # TODO: figure out how to display and expose this without spamming discord
            segment_name = f"{self.name} (Step {i}/{len(self.values)}: {value})"
            segment_uid = f"{self.uid}_step_{i}"
            segment_config = self.segment_constants
            segment_config[self.segment_variable] = value
            self.segments.append(
                self.segment_class(
                    segment_uid, segment_name, segment_config, self._testbench_manager
                )
            )

    def run(self):
        for segment in self.segments:
            segment.run()

    def generate_report(self):
        pass
