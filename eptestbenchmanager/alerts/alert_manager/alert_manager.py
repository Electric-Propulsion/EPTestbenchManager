from abc import ABC, abstractmethod
from typing import Union
from eptestbenchmanager.chat.engine import CommunicationEngine
from eptestbenchmanager.chat.alert_manager.alert_severity import AlertSeverity


class AlertManager(ABC):
    """
    AlertManager is an abstract base class that defines the interface for sending alerts
    using a communication engine.
    Attributes:
        _engine (CommunicationEngine): The communication engine used to send alerts.
    """

    def __init__(self, engine: CommunicationEngine):
        self._engine = engine

    @abstractmethod
    def send_alert(
        self, message: str, severity: AlertSeverity, target: Union[str, None] = None
    ) -> None:
        """
        Sends an alert with the specified message and severity.
        Args:
            message (str): The message to be sent in the alert.
            severity (AlertSeverity): The severity level of the alert.
            target (Union[str, None], optional): The target recipient of the alert. Defaults to None
        Raises:
            NotImplementedError: This method is intended to be overridden in a subclass.
        """
        raise NotImplementedError("Trying to send an alert from an abstract class.")
