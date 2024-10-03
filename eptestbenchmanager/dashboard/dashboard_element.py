from typing import Any


class DashboardElement:
    def __init__(self, uid: str, testbench_manager: "TestbenchManager"):
        self.uid = (uid,)
        self._testbench_manager = testbench_manager

    @property
    def children(self) -> list:  # list of what??
        pass

    def callback(self, value: Any) -> None:
        pass
