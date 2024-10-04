from threading import Thread
from eptestbenchmanager.dashboard import DashboardView
from .experiment_segments.experiment_segment import ExperimentSegment, AbortingSegmentFailure
from io import StringIO


class Experiment:

    def __init__(
        self, uid: str, name: str, description: str, segments: list[ExperimentSegment], view: DashboardView
    ):
        self.uid: str = uid
        self.name: str = name
        self.description: str = description
        self.segments: list[ExperimentSegment] = segments
        self.view = view

    def run(self):
        self._runner_thread = Thread(
            target=self.run_segments, name=f"{self.uid} Runner Thread", daemon=False
        )
        self._runner_thread.start()

    def run_segments(self) -> None:
        for segment in self.segments:
            try:
                segment.run()
                print(segment.data)
            except AbortingSegmentFailure as e:
                # TODO: indicate somehow that we're aborting
                print(e)
                print(segment.data)
                return

    def generate_report(self) -> StringIO:
        for segment in self.segments:
            segment.generate_report()
        # TODO: return the report

    @property
    def rules(self):
        pass  # TODO: need to get just the rule from the active segment?
