from os import path, walk
from pathlib import Path

from eptestbenchmanager.connections import ConnectionManager
from eptestbenchmanager.monitor import TestbenchMonitor
from eptestbenchmanager.experiment_runner import ExperimentRunner


class TestbenchManager:

    def __init__(self):
        self.monitor: TestbenchMonitor = None
        self.connection_manager: ConnectionManager = None
        # self.alert_manager = AlertManager()
        # self.communication_engine = CommunicationEngine()
        # self.chat_manager = ChatManager()
        # self.dashboard_manager = DashboardManager()
        self.runner: ExperimentRunner = None

    def start_app(
        self,
        delay_apparatus_load: bool = False,
        delay_experiment_load: bool = False,
    ):

        # Initialize the connection manager
        if not delay_apparatus_load:
            # Assume apparatus config is in ../config/apparatus_config.yaml
            apparatus_config_file_path = path.join(
                Path(__file__).parent.parent, Path("config/apparatus_config.yaml")
            )
        else:
            apparatus_config_file_path = None
        self.connection_manager = ConnectionManager(apparatus_config_file_path)

        # Initialize the experiment runner
        self.runner = ExperimentRunner()

        if not delay_experiment_load:
            # Load all the experiments in /experiment_config
            experiment_config_dir_path = path.join(
                Path(__file__).parent.parent, Path("experiment_config")
            )
            for dirpath, _, filenames in walk(experiment_config_dir_path):
                for filename in filenames:
                    if filename.endswith(".yaml"):
                        with open(
                            path.join(dirpath, filename), "r", encoding="utf-8"
                        ) as experiment_config_file:
                            self.runner.add_experiment(experiment_config_file)

        # Start everything
        self.connection_manager.run()

        self.runner.run_experiment("pumpdown_measure_leaks")
