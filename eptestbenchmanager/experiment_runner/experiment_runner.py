from io import StringIO
from .experiment import Experiment
from .experiment_factory import ExperimentFactory


class ExperimentRunner:

    def __init__(self, testbench_manager: 'TestbenchManager'):
        self._experiments: dict[str, Experiment] = {}
        self._testbench_manager = testbench_manager

    def add_experiment(self, experiment_file: StringIO) -> None:
        experiment = ExperimentFactory.create_experiment(experiment_file, self._testbench_manager)
        self._experiments[experiment.uid] = experiment

    def run_experiment(self, uid: str) -> None:
        self._experiments[uid].run()
        # generating reports should occur here too

    def remove_experiment(self, uid: str) -> None:
        self._experiments.pop(uid)

    @property 
    def views(self):
        return [experiment.view for experiment in self._experiments.values()]

    @property
    def experiments(self) -> dict[str, Experiment]:
        return self._experiments.keys()
