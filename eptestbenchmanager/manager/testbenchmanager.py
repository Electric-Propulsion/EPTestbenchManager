from os import path, walk
from pathlib import Path
from time import sleep

from eptestbenchmanager.connections import ConnectionManager
from eptestbenchmanager.monitor import TestbenchMonitor
from eptestbenchmanager.experiment_runner import ExperimentRunner
from eptestbenchmanager.chat.alert_manager import DiscordAlertManager
from eptestbenchmanager.chat.engine import DiscordEngine
from eptestbenchmanager.chat.chat_manager import DiscordChatManager
from eptestbenchmanager.dashboard import DashboardManager
from eptestbenchmanager.report import ReportManager


class TestbenchManager:
    """Manages the testbench operations including connections, monitoring, and communication.

    Attributes:
        monitor (TestbenchMonitor): Monitors the testbench and evaluates rules.#TODO: Implement this
        connection_manager (ConnectionManager): Manages connections with physical and virtual
        instruments.
        communication_engine (DiscordEngine): Engine that plugs into alert and chat managers.
        alert_manager (DiscordAlertManager): Manages sending alerts.
        chat_manager (DiscordChatManager): Manages chat commands and responses.
        runner (ExperimentRunner): Runs experiments.
        dashboard (DashboardManager): Manages the web GUI dashboard.
        report_manager (ReportManager): Manages reports/archives. #TODO: not implemented yet
    """

    def __init__(self):
        """Initializes the TestbenchManager with default attributes."""
        self.monitor: TestbenchMonitor = None
        self.connection_manager: ConnectionManager = None
        self.communication_engine = DiscordEngine()
        self.alert_manager = DiscordAlertManager(self.communication_engine)
        self.chat_manager = DiscordChatManager(self.communication_engine, self)
        self.runner: ExperimentRunner = None
        self.dashboard: DashboardManager = DashboardManager(self)
        self.report_manager = ReportManager(self)

    def start_app(
        self,
        delay_apparatus_load: bool = False,
        delay_experiment_load: bool = False,
        discord_guild: str = "Hall-Effect Thruster",
    ):
        """Starts the application with optional delays for loading apparatus and experiments.

        Args:
            delay_apparatus_load (bool): If True, delays loading the apparatus configuration.
            delay_experiment_load (bool): If True, delays loading the experiment configurations.
            discord_guild (str): The Discord guild name for communication.
        """

        # Initialize the connection manager
        if not delay_apparatus_load:
            apparatus_config_file_path = path.join(
                Path(__file__).parent.parent, Path("config/apparatus_config.yaml")
            )
        else:
            apparatus_config_file_path = None

        # Initialize the experiment runner
        self.runner = ExperimentRunner(self)

        self.connection_manager = ConnectionManager(self, apparatus_config_file_path)

        # Configure the chat stuff
        self.chat_manager.configure()

        # Start everything
        self.connection_manager.run()
        self.communication_engine.run()
        sleep(2.5)  # just give it a little time to start up
        self.communication_engine.configure({"guild": discord_guild})

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

        # Start the dashboard
        self.dashboard.configure()
        self.dashboard.run()

        while True:
            sleep(1)
