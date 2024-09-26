from abc import ABC, abstractmethod


class CommunicationEngine(ABC):

    @abstractmethod
    def send_message(self, message: str, channel: str) -> None:
        raise NotImplementedError("Trying to send a message from an abstract class.")

    @abstractmethod
    def configure(self, config: dict) -> None:
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError("Trying to run an abstract class.")
