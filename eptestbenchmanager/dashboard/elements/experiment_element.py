from . import DashboardElement

class ExperimentElement(DashboardElement):
    
    def __init__(self, uid: str, title: str, testbench_manager: "TestbenchManager", experiment: "Experiment"):
        super().__init__(uid, title, testbench_manager)
        self._experiment = experiment