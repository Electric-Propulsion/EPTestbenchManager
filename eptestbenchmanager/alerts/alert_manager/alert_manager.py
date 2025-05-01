from typing import Union
import logging
from eptestbenchmanager.alerts.engine import DiscordEngine, StdoutEngine
from eptestbenchmanager.alerts.alert_manager.alert_severity import AlertSeverity
import time

logger = logging.getLogger(__name__)


class AlertManager:
    """
    AlertManager is an abstract base class that defines the interface for sending alerts
    using a communication engine.
    Attributes:
        _engine (CommunicationEngine): The communication engine used to send alerts.
    """

    def __init__(self, testbench_manager) -> None:
        """Initializes the AlertManager with a communication engine."""
        self.testbench_manager = testbench_manager
        engine_types = self.testbench_manager.runtime_manager.configs[
            "alert_config"
        ].keys()
        self._engines = []
        for engine_type in engine_types:
            match engine_type:
                case "discord":
                    logger.info("Initializing Discord engine")
                    try:
                        engine = DiscordEngine(self.testbench_manager)
                        engine.run()
                        time.sleep(2.5)  # Give the engine time to initialize
                        engine.configure()
                        self._engines.append(engine)
                    except Exception as e:
                        logger.critical(f"Failed to initialize Discord engine: {e}")
                
                case "stdout":
                    logger.info("Initializing Stdout engine")
                    try:

                        engine = StdoutEngine(self.testbench_manager)
                        engine.run()
                        engine.configure(None)
                        self._engines.append(engine)
                    except Exception as e:
                        logger.critical(f"Failed to initialize Stdout engine: {e}")

                case _:
                    logger.warning(f"Unknown engine type: {engine_type}")
                    continue

        self._operators: list[str] = []  # Operator string identifiers
        for engine in self._engines:
            self._operators.extend(engine.operators)

    def send_message(
        self,
        message: str,
        severity: AlertSeverity,
        target_operators: Union[str, list[str], None] = None,
    ) -> None:
        """
        Sends an alert message.

        Args:
            message (str): The alert message to send.
            severity (AlertSeverity): The severity level of the alert.
            target_operator (Union[str, list[str], None], optional): The target operator(s) to mention.
                Defaults to None.
        """
        for engine in self._engines:
            engine.send_message(message, severity, target_operators)

    def send_file(
        self,
        file_path: str,
        severity: AlertSeverity,
    ) -> None:
        """
        Sends a file.

        Args:
            file_path (str): The path to the file to send.
            severity (AlertSeverity): The severity level of the alert.
        """
        for engine in self._engines:
            engine.send_file(file_path, severity)

    @property
    def operators(self) -> list[str]:
        """
        Returns a list of operator string identifiers.

        Returns:
            list[str]: List of operator string identifiers.
        """
        return self._operators
