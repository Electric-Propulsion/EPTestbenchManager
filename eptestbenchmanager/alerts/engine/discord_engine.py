import asyncio
import logging
from threading import Thread
import discord
import os
from typing import Union
from . import DiscordClient
from . import CommunicationEngine
from eptestbenchmanager.alerts.alert_manager import AlertSeverity

logger = logging.getLogger(__name__)


class DiscordEngine(CommunicationEngine):
    """A communication engine for interacting with Discord.

    Attributes:
        _client (DiscordClient): The Discord client instance.
        _token (str): The bot token for authentication.
        _guild_id (str): The ID of the guild (server) to connect to.
        _user_ids (dict): A dictionary mapping user names to their IDs.
        _channel_ids (dict): A dictionary mapping channel names to their IDs.
        _loop (asyncio.AbstractEventLoop): The event loop for asynchronous operations.
        _client_thread (Thread): The thread running the Discord client.
    """

    def __init__(self, testbench_manager) -> None:
        """Initializes the DiscordEngine with default intents and creates a new event loop."""
        super().__init__(testbench_manager)
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self._client = DiscordClient(intents=intents)
        self._token = os.getenv("DISCORD_TOKEN")
        if self._token is None:
            raise ValueError("DISCORD_TOKEN environment variable not set")
        self._guild_id = None
        self._user_ids = None
        self._channel_ids = None
        self._loop = asyncio.new_event_loop()
        self._client_thread: Thread = None

    def send_message(
        self,
        message: str,
        severity: AlertSeverity,
        target: Union[str, list[str], None] = None,
    ) -> None:
        """Sends an alert message to a Discord channel.

        Args:
            message (str): The alert message to send.
            severity (AlertSeverity): The severity level of the alert.
            target (Union[str, list[str], None], optional): The target user(s) to mention.
            Defaults to None.
        """
        target_str = ""
        if target is not None:
            try:
                if isinstance(target, str):
                    target_str = f"<@{self.users[target]}>"
                else:
                    target_str = " ".join([f"<@{self.users[user]}>" for user in target])
            except KeyError:
                # TODO: We should do something better than this. You shouldn't be FORCED to have alerts.
                logger.warning(
                    "Failed to send alert to %s (not in known users).", target
                )
            except TypeError:
                logger.warning("Failed to send alert (No users are known).")

        prefix = self.get_prefix(severity)
        channel = self.get_channel(severity)

        composed_message = f"{prefix} {target_str}\n{message}"

        self._send_message(composed_message, channel)

    def send_file(
        self,
        file_path: str,
        severity: AlertSeverity,
    ) -> None:
        """Sends a file to a Discord channel.

        Args:
            file_path (str): The path to the file to send.
            severity (AlertSeverity): The severity level of the alert.
        """
        channel = self.get_channel(severity)

        self._send_file(file_path, channel)

    def get_prefix(self, severity: str) -> AlertSeverity:
        """Gets the prefix emoji for a given severity level.

        Args:
            severity (str): The severity level.

        Returns:
            AlertSeverity: The corresponding emoji for the severity level.
        """
        match severity:
            case AlertSeverity.INFO:
                return ":information_source:"
            case AlertSeverity.CAUTION:
                return ":warning:"
            case AlertSeverity.WARNING:
                return ":bangbang:"
            case _:
                return ":grey_question:"

    def get_channel(self, severity: str) -> str:
        """Gets the Discord channel for a given severity level.

        Channels are hardcoded. This method should be updated if the Discord server changes.

        Args:
            severity (str): The severity level.

        Returns:
            str: The corresponding Discord channel for the severity level.
        """
        match severity:
            case "info":
                return self._config["channels"]["info"]
            case "caution":
                return self._config["channels"]["caution"]
            case "warning":
                return self._config["channels"]["warning"]
            case _:
                return self._config["channels"]["default"]

    def _send_message(self, message: str, channel: str) -> None:
        """Sends a message to a specified channel.

        Args:
            message (str): The message to send.
            channel (str): The name of the channel to send the message to.
        """
        logger.info("Sending message: %s", message)
        asyncio.run_coroutine_threadsafe(
            self._client.send_message(message, self._channel_ids[channel]), self._loop
        )

    def _send_file(self, file_path: str, channel: str) -> None:
        """Sends a file to a specified channel.

        Args:
            file_path (str): The path to the file to send.
            channel (str): The name of the channel to send the file to.
        """
        asyncio.run_coroutine_threadsafe(
            self._client.send_file(file_path, self._channel_ids[channel]), self._loop
        )

    def run(self) -> None:
        """Starts the Discord client in a separate thread."""
        self._client_thread = Thread(
            target=self._run_client, name="Discord Client Thread", daemon=True
        )
        self._client_thread.start()

    def configure(self) -> None:
        """Configures the Discord engine with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """

        self._config = self.testbench_manager.runtime_manager.configs["alert_config"][
            "discord"
        ]

        self._guild_id = int(self._config["guild"])
        logger.info("Connecting to guild %s", self._guild_id)
        self._user_ids = self._get_user_ids()
        self._channel_ids = self._get_channel_ids()

    def _run_client(self) -> None:
        """Runs the Discord client using the event loop."""
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._client.start(self._token))
        except (
            Exception
        ) as e:  # yes I know it's too broad, but I'm not sure what exceptions can be raised here
            logger.error("Error running Discord client: %s", e)

    def _get_user_ids(self) -> dict[str, int]:
        """Retrieves a dictionary of user names and their IDs for the current guild.

        Returns:
            dict: A dictionary mapping user names to their IDs.

        Raises:
            ValueError: If the guild ID is not set.
        """
        if self._guild_id is not None:
            users = {}
            for user in self._client.get_guild(self._guild_id).members:
                users[user.name] = user.id
            return users
        raise ValueError("Guild ID not set")

    @property
    def users(self) -> dict[str, int]:
        """Gets the dictionary of user names and their IDs.

        Returns:
            dict: A dictionary mapping user names to their IDs.
        """
        return self._user_ids

    @property
    def operators(self) -> list[str]:
        """Gets the list of operator string identifiers.

        Returns:
            list: A list of operator string identifiers.
        """
        if self._user_ids is None:  # If the user IDs are not set, return an empty list
            return []
        print(list(self._user_ids.keys()))
        return list(self._user_ids.keys())

    def _get_channel_ids(self) -> dict[str, int]:
        """Retrieves a dictionary of channel names and their IDs for the current guild.

        Returns:
            dict: A dictionary mapping channel names to their IDs.

        Raises:
            ValueError: If the guild ID is not set.
        """
        if self._guild_id is not None:
            channels = {}
            for channel in self._client.get_guild(self._guild_id).channels:
                channels[channel.name] = channel.id
            return channels
        raise ValueError("Guild ID not set")
