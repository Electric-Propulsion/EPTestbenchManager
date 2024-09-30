from abc import ABC, abstractmethod
from threading import Thread, Lock

from eptestbenchmanager.monitor import Rule

class AbortingSegmentFailure(Exception):
    # If this is raised, the experment should teminate
    pass


class ExperimentSegment(ABC):

    def __init__(self, uid: str, config: dict, testbench_manager: 'TestbenchManager'):
        self.uid = uid
        self._rules: list[Rule] = []
        self._runner_thread: Thread = None
        self._testbench_manager = testbench_manager
        self.data = None
        self.configure(config)

    @abstractmethod
    def configure(self, config: dict):
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError("Trying to run an abstract class!")

    @abstractmethod
    def generate_report(self):  # TODO: return type?
        raise NotImplementedError("Trying to generate a report from an abstract class.")

    @property
    def rules(self) -> list[Rule]:
        return self._rules
