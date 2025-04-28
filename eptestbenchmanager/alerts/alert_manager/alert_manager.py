from typing import Union
from eptestbenchmanager.alerts.engine import CommunicationEngine
from eptestbenchmanager.alerts.alert_manager.alert_severity import AlertSeverity


class AlertManager:
    """
    AlertManager is an abstract base class that defines the interface for sending alerts
    using a communication engine.
    Attributes:
        _engine (CommunicationEngine): The communication engine used to send alerts.
    """

    def __init__(
        self, engines: Union[CommunicationEngine, list[CommunicationEngine]]
    ) -> None:
        self._engines = engines if isinstance(engines, list) else [engines]
        self._operators: list[str] = []  # Operator string identifiers
        self._operators.extend(engine.operators for engine in self._engines)

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
