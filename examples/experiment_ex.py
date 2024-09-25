from eptestbenchmanager.experiment_runner import ExperimentRunner
from os.path import join
from pathlib import Path

runner = ExperimentRunner()
# Assume it's in ../eptestbenchmanager/experiment_config/pumpdown_measure_leaks.yaml
config_file_path = join(
    Path(__file__).parent.parent,
    Path("eptestbenchmanager/experiment_config/pumpdown_measure_leaks.yaml"),
)
print(config_file_path)  # TODO: make this a logging call

with open(config_file_path, "r", encoding="utf-8") as f:
    runner.add_experiment(f)

runner.run_experiment("pumpdown_measure_leaks")
print("I'm the main thread!")
