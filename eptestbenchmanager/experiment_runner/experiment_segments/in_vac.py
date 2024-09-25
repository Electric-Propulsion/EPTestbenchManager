from . import ExperimentSegment
from abc import ABC, abstractmethod


class InVac(ExperimentSegment):
    @abstractmethod
    def configure(self, config: dict):
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def generate_report(self):
        pass
