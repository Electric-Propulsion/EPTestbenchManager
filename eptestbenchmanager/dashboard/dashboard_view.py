from typing import Any


class DashboardView:
    def __init__(self, uid: str, title: str, testbench_manager: "TestbenchManager"):
        self.uid = uid
        self.title = title
        self._testbench_manager = testbench_manager

    @property
    def layout(self) -> Any:  # TODO
        pass

    def callback(self, value: Any) -> None:  # TODO: why?
        pass
