from os import path, walk
from pathlib import Path
from time import sleep

from eptestbenchmanager.connections import ConnectionManager
from eptestbenchmanager.monitor import TestbenchMonitor
from eptestbenchmanager.experiment_runner import ExperimentRunner
from eptestbenchmanager.chat.alert_manager import DiscordAlertManager, AlertSeverity
from eptestbenchmanager.chat.engine import DiscordEngine
from eptestbenchmanager.chat.chat_manager import DiscordChatManager
from eptestbenchmanager.dashboard import DashboardManager, get_home_view


class TestbenchManager:

    def __init__(self):
        self.monitor: TestbenchMonitor = None
        self.connection_manager: ConnectionManager = None
        self.communication_engine = DiscordEngine()
        self.alert_manager = DiscordAlertManager(self.communication_engine)
        self.chat_manager = DiscordChatManager(self.communication_engine, self)
        self.dashboard_manager = DashboardManager(self)
        self.runner: ExperimentRunner = None

    def start_app(
        self,
        delay_apparatus_load: bool = False,
        delay_experiment_load: bool = False,
        discord_guild: str = "Festus's bot test server",
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
        self.runner = ExperimentRunner(self)

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

        # Configure the chat stuff
        self.chat_manager.configure()

        # Start everything
        self.connection_manager.run()

        self.communication_engine.run()
        sleep(10)  # just give it a little time to start up
        self.communication_engine.configure({"guild": discord_guild})

        self.dashboard_manager.run()
        self.dashboard_manager.add_view(get_home_view(self))
        while True:
            sleep(1)
