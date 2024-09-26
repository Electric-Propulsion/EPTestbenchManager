from abc import ABC, abstractmethod
from typing import Union
from eptestbenchmanager.chat.engine import CommunicationEngine
from . import AlertSeverity

class AlertManager(ABC):

    def __init__(self, engine: CommunicationEngine):
        self._engine = engine

    @abstractmethod
    def send_alert(self, message: str, severity: AlertSeverity, target: Union[str, None] = None) -> None:
        raise NotImplementedError("Trying to send an alert from an abstract class.")
