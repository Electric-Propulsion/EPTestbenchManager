import discord
import asyncio
from threading import Thread
from . import DiscordClient
from . import CommunicationEngine


class DiscordEngine(CommunicationEngine):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        self._client = DiscordClient(intents=intents)
        self._token = "MTI4Njc4NTAwNzgzODQzMzM0MQ.GG3EFH.S9HbRrmv62qIIiD0wIUH1CVyoL0ERDmF4H_M2g"  # TODO: jezus don't put your token in the code
        self._guild_id = None
        self._user_ids = None
        self._channel_ids = None
        self._loop = asyncio.new_event_loop()
        self._client_thread: Thread = None

    def configure_message_processor(self, process_message: callable) -> None:
        self._client.configure_message_processor(process_message)

    def send_message(self, message: str, channel: str) -> None:
        print(f"Sending message: {message}")
        asyncio.run_coroutine_threadsafe(
            self._client.send_message(message, self._channel_ids[channel]), self._loop
        )

    def send_file(self, file_path: str, channel: str) -> None:
        asyncio.run_coroutine_threadsafe(
            self._client.send_file(file_path, self._channel_ids[channel]), self._loop
        )

    def run(self) -> None:
        self._client_thread = Thread(
            target=self._run_client, name="Discord Client Thread", daemon=True
        )
        self._client_thread.start()

    def configure(self, config: dict) -> None:
        guild_ids = self._get_guild_ids()
        print("=======")
        print(guild_ids)
        print(config["guild"])
        if config["guild"] not in guild_ids:
            raise ValueError("Guild not found")
        self._guild_id = guild_ids[config["guild"]]

        self._user_ids = self._get_user_ids()
        self._channel_ids = self._get_channel_ids()

    def _run_client(self) -> None:
        asyncio.set_event_loop(self._loop)
        self._loop.run_until_complete(self._client.start(self._token))

    def _get_guild_ids(self) -> list[str, int]:
        guilds = {}
        for guild in self._client.guilds:
            guilds[guild.name] = guild.id
            print(f"Found guild: {guild.name} ({guild.id})")
        return guilds

    def _get_user_ids(self) -> dict[str, int]:
        if self._guild_id is not None:
            users = {}
            for user in self._client.get_guild(self._guild_id).members:
                users[user.name] = user.id
            return users
        raise ValueError("Guild ID not set")

    @property
    def users(self) -> dict[str, int]:
        return self._user_ids

    def _get_channel_ids(self) -> dict[str, int]:
        if self._guild_id is not None:
            channels = {}
            for channel in self._client.get_guild(self._guild_id).channels:
                channels[channel.name] = channel.id
            return channels
        raise ValueError("Guild ID not set")
