from . import DashboardElement


class ExperimentElement(DashboardElement):

    def __init__(
        self,
        uid: str,
        title: str,
        testbench_manager: "TestbenchManager",
        experiment_uid: str,
    ):
        super().__init__(uid, title)
        self._experiment_runner = testbench_manager.runner
        self._experiment_uid = experiment_uid
