from abc import ABC, abstractmethod


class CommunicationEngine(ABC):
    """Abstract base class for communication engines.

    This class defines the interface for communication engines, including methods for sending
    messages, configuring the engine, and running the engine.
    """

    @abstractmethod
    def send_message(self, message: str, channel: str) -> None:
        """Sends a message to a specified channel.

        Args:
            message (str): The message text to send.
            channel (str): The channel where the message will be sent.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to send a message from an abstract class.")

    # TODO: Check if this is actually used??
    @abstractmethod
    def configure(self, config: dict) -> None:
        """Configures the communication engine with the provided settings.

        Args:
            config (dict): A dictionary containing configuration settings.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to configure an abstract class.")

    @abstractmethod
    def run(self) -> None:
        """Runs the communication engine.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to run an abstract class.")
