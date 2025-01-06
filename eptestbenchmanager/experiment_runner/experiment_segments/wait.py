import time
from . import ExperimentSegment


class Wait(ExperimentSegment):
    """Wait segment for an experiment.

    This class represents a wait segment in an experiment, where the system pauses for a specified
    number of seconds.
    """

    def configure(self, config: dict):
        """Configures the wait segment.

        Args:
            config (dict): Configuration dictionary containing the number of seconds to wait.
        """
        self.seconds = config["seconds"]

    def run(self) -> None:
        """Executes the wait segment.

        This method pauses the execution for the configured number of seconds.
        """
        time.sleep(self.seconds)

    def generate_report(self):
        """Generates a report for the wait segment.

        This method is currently a placeholder and does not generate any report.
        """
