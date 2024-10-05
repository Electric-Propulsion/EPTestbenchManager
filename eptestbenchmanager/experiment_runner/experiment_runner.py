from io import StringIO
from threading import Lock
from .experiment import Experiment
from .experiment_factory import ExperimentFactory


class ExperimentRunner:

    def __init__(self, testbench_manager: "TestbenchManager"):
        self._experiments: dict[str, Experiment] = {}
        self._testbench_manager = testbench_manager
        self._experiment_lock = Lock()

    def add_experiment(self, experiment_file: StringIO) -> None:
        experiment = ExperimentFactory.create_experiment(
            experiment_file, self._testbench_manager, self._experiment_lock
        )
        self._experiments[experiment.uid] = experiment

    def run_experiment(self, uid: str) -> None:
        if self._experiment_lock.acquire(blocking=False):
            print("Running experiment")
            self._experiments[uid].run()
        else:
            print("No can do. Experiment is already running")
        # generating reports should occur here too

    def remove_experiment(self, uid: str) -> None:
        self._experiments.pop(uid)

    def get_experiment_segments(self, experiment_uid: str) -> list:
        return self._experiments[experiment_uid].segments

    def get_experiment_current_segment_id(self, experiment_uid: str) -> int:
        return self._experiments[experiment_uid].current_segment_id

    @property
    def views(self):
        return [experiment.view for experiment in self._experiments.values()]

    @property
    def experiments(self) -> dict[str, Experiment]:
        return self._experiments.keys()
