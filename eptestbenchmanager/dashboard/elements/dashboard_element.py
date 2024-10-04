from typing import Any
from abc import ABC, abstractmethod


class DashboardElement(ABC):
    def __init__(self, uid: str, title: str, testbench_manager: "TestbenchManager"):
        self.uid = uid
        self.title = title
        self._testbench_manager = testbench_manager

    @abstractmethod
    def div(self) -> list:  # list of what??
        pass

    @abstractmethod
    def register_callbacks(self) -> None:
        pass
