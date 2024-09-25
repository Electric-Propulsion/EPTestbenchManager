from . import ExperimentSegment
import time


class Pumpdown(ExperimentSegment):

    def configure(self, config: dict):
        pass

    def run_segment(self) -> None:
        print("Howdy! I'm running the pumpdown segment.")
        time.sleep(10)
        print("I'm done running the pumpdown segment.")

    def generate_report(self):
        pass
