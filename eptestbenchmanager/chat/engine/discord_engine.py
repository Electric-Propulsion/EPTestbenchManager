import asyncio
import logging
from threading import Thread
import discord
from . import DiscordClient
from . import CommunicationEngine

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

    def __init__(self):
        """Initializes the DiscordEngine with default intents and creates a new event loop."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self._client = DiscordClient(intents=intents)
        self._token = "MTI4Njc4NTAwNzgzODQzMzM0MQ.GG3EFH.S9HbRrmv62qIIiD0wIUH1CVyoL0ERDmF4H_M2g"  # TODO: jezus don't put your token in the code #pylint: disable=line-too-long
        self._guild_id = None
        self._user_ids = None
        self._channel_ids = None
        self._loop = asyncio.new_event_loop()
        self._client_thread: Thread = None

    def configure_message_processor(self, process_message: callable) -> None:
        """Configures the message processor for the Discord client.

        Args:
            process_message (callable): A callable to process incoming messages.
        """
        self._client.configure_message_processor(process_message)

    def send_message(self, message: str, channel: str) -> None:
        """Sends a message to a specified channel.

        Args:
            message (str): The message to send.
            channel (str): The name of the channel to send the message to.
        """
        logger.info("Sending message: %s", message)
        asyncio.run_coroutine_threadsafe(
            self._client.send_message(message, self._channel_ids[channel]), self._loop
        )

    def send_file(self, file_path: str, channel: str) -> None:
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

    def configure(self, config: dict) -> None:
        """Configures the Discord engine with the provided configuration.

        Args:
            config (dict): A dictionary containing configuration parameters.
        """
        guild_ids = self._get_guild_ids()
        logger.info("Aware of guilds %s", guild_ids)
        logger.info("Connecting to guild %s", config["guild"])
        if config["guild"] not in guild_ids:
            raise ValueError("Guild not found")
        self._guild_id = guild_ids[config["guild"]]

        self._user_ids = self._get_user_ids()
        self._channel_ids = self._get_channel_ids()

    def _run_client(self) -> None:
        """Runs the Discord client using the event loop."""
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._client.start(self._token))

    def _get_guild_ids(self) -> list[str, int]:
        """Retrieves a dictionary of guild names and their IDs.

        Returns:
            dict: A dictionary mapping guild names to their IDs.
        """
        guilds = {}
        for guild in self._client.guilds:
            guilds[guild.name] = guild.id
            logger.info("Found guild: %s (%s)", guild.name, guild.id)
        return guilds

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
