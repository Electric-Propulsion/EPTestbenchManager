from abc import ABC, abstractmethod


class AlertManager(ABC):

    @abstractmethod
    def send_alert(self, message: str) -> None:
        raise NotImplementedError("Trying to send an alert from an abstract class.")
