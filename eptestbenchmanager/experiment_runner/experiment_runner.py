from io import StringIO
from .experiment import Experiment
from .experiment_factory import ExperimentFactory


class ExperimentRunner:

    def __init__(self):
        self._experiments: dict[str, Experiment] = {}

    def add_experiment(self, experiment_file: StringIO) -> None:
        experiment = ExperimentFactory.create_experiment(experiment_file)
        self._experiments[experiment.uid] = experiment

    def run_experiment(self, uid: str) -> None:
        self._experiments[uid].run()
        # generating reports should occur here too

    def remove_experiment(self, uid: str) -> None:
        self._experiments.pop(uid)

    @property
    def experiments(self) -> dict[str, Experiment]:
        return self._experiments.keys()
