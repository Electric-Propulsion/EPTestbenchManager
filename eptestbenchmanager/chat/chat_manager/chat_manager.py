from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from eptestbenchmanager.chat.engine import CommunicationEngine

if TYPE_CHECKING:
    from eptestbenchmanager.manager import TestbenchManager


class ChatManager(ABC):
    """Abstract base class for managing chat interactions.

    This class defines the interface for configuring the chat manager and processing messages.
    """

    def __init__(
        self, engine: CommunicationEngine, testbench_manager: "TestbenchManager"
    ):
        """Initializes the ChatManager with a communication engine and a testbench manager.

        Args:
            engine (CommunicationEngine): The communication engine for handling chat interactions.
            testbench_manager (TestbenchManager): The manager for the testbench.
        """
        self.testbench_manager = testbench_manager
        self._engine = engine

    @abstractmethod
    def configure(self) -> None:
        """Configures the chat manager.

        This method should be implemented by subclasses to set up necessary configurations.

        Raises:
            NotImplementedError: If called on the abstract base class.
        """
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def process_message(self, message: str, channel: str, user: int) -> None:
        """Processes a chat message.

        This method should be implemented by subclasses to handle incoming messages.

        Args:
            message (str): The message content.
            channel (str): The channel from which the message was received.
            user (int): The ID of the user who sent the message.

        Raises:
            NotImplementedError: If called on the abstract base class.
        """
        raise NotImplementedError("Trying to process a message from an abstract class.")
