from .experiment_segments.experiment_segment import ExperimentSegment
from io import StringIO


class Experiment:

    def __init__(
        self, uid: str, name: str, description: str, segments: list[ExperimentSegment]
    ):
        self.uid: str = uid
        self.name: str = name
        self.description: str = description
        self.segments: list[ExperimentSegment] = segments

    def run(self) -> None:
        for segment in self.segments:
            segment.run()

    def generate_report(self) -> StringIO:
        for segment in self.segments:
            segment.generate_report()
        # TODO: return the report

    @property
    def rules(self):
        pass  # TODO: need to get just the rule from the active segment?
