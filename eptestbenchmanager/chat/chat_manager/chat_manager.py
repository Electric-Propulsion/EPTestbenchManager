from abc import ABC, abstractmethod


class ChatManager(ABC):

    @abstractmethod
    def configure(self) -> None:
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def process_message(self, message: str) -> None:
        raise NotImplementedError("Trying to process a message from an abstract class.")
