import time
from . import ExperimentSegment


class Wait(ExperimentSegment):
    def configure(self, config: dict):
        self.seconds = config["seconds"]

    def run(self) -> None:
        time.sleep(self.seconds)

    def generate_report(self):
        pass
