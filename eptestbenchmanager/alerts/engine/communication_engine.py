from abc import ABC, abstractmethod

from typing import Union
from eptestbenchmanager.alerts.alert_manager.alert_severity import AlertSeverity


class CommunicationEngine(ABC):
    """Abstract base class for communication engines.

    This class defines the interface for communication engines, including methods for sending
    messages, configuring the engine, and running the engine.
    """

    def __init__(self, testbench_manager) -> None:
        """Initializes the communication engine with a testbench manager.

        Args:
            testbench_manager: The testbench manager instance.
        """
        self.testbench_manager = testbench_manager

    @abstractmethod
    def send_message(
        self,
        message: str,
        severity: AlertSeverity,
        target: Union[str, list[str], None] = None,
    ) -> None:
        """Sends a message to a specified channel.

        Args:
            message (str): The message text to send.
            channel (str): The channel where the message will be sent.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to send a message from an abstract class.")

    @abstractmethod
    def send_file(
        self,
        file_path: str,
        severity: AlertSeverity,
    ) -> None:
        """Sends a file to a specified channel.

        Args:
            file_path (str): The path to the file to send.
            severity (str): The severity level of the alert.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to send a file from an abstract class.")

    @property
    @abstractmethod
    def operators(self) -> list[str]:
        """Returns a list of operator string identifiers.

        Raises:
            NotImplementedError: If the method is called from the abstract class.
        """
        raise NotImplementedError("Trying to get operators from an abstract class.")

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
