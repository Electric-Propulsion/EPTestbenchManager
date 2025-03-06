from os import path, walk
from pathlib import Path
from time import sleep
import logging

from eptestbenchmanager.connections import ConnectionManager
from eptestbenchmanager.monitor import TestbenchMonitor
from eptestbenchmanager.experiment_runner import ExperimentRunner
from eptestbenchmanager.chat.alert_manager import DiscordAlertManager
from eptestbenchmanager.chat.engine import DiscordEngine
from eptestbenchmanager.chat.chat_manager import DiscordChatManager
from eptestbenchmanager.dashboard import DashboardManager
from eptestbenchmanager.report import ReportManager
from eptestbenchmanager.estop.estop import EStop

logger = logging.getLogger(__name__)


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
        self.estop = EStop()

    def start_app(
        self,
        discord_guild: str = "Hall-Effect Thruster",
    ):
        """Starts the application with optional delays for loading apparatus and experiments.

        Args:
            delay_apparatus_load (bool): If True, delays loading the apparatus configuration.
            delay_experiment_load (bool): If True, delays loading the experiment configurations.
            discord_guild (str): The Discord guild name for communication.
        """

        # Initialize the connection manager
        apparatus_config_dir_path = Path(
            path.join(Path(__file__).parent.parent, Path("apparatus_config"))
        )

        experiment_config_dir_path = Path(
            path.join(Path(__file__).parent.parent, Path("experiment_config"))
        )

        # Initialize the experiment runner
        self.runner = ExperimentRunner(self, experiment_config_dir_path)

        self.connection_manager = ConnectionManager(self, apparatus_config_dir_path)

        # Configure the chat stuff
        try:
            self.chat_manager.configure()
            self.communication_engine.run()
            sleep(2.5)  # just give it a little time to start up
            self.communication_engine.configure({"guild": discord_guild})
        except Exception as e:  # I know it's way too broad
            logger.critical(
                "Discord failed to start. No messages will be sent or recieved."
            )

        # Start everything
        self.connection_manager.run()

        # Start the dashboard
        self.dashboard.configure()
        self.dashboard.run()

        # Reset the EStop
        self.estop.estop_reset(force=True)

        while True:
            sleep(1)
