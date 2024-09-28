from abc import ABC, abstractmethod
from eptestbenchmanager.chat.engine import CommunicationEngine


class ChatManager(ABC):

    def __init__(self, engine: CommunicationEngine, testbench_manager: 'TestbenchManager'):
        self.testbench_manager = testbench_manager
        self._engine = engine

    @abstractmethod
    def configure(self) -> None:
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def process_message(self, message: str, channel: str, user: int) -> None:
        raise NotImplementedError("Trying to process a message from an abstract class.")
