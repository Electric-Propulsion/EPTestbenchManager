import discord
import asyncio
from threading import Thread
from . import DiscordClient
from . import CommunicationEngine


class DiscordEngine(CommunicationEngine):

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = DiscordClient(intents=intents)
        self.token = "MTI4Njc4NTAwNzgzODQzMzM0MQ.GG3EFH.S9HbRrmv62qIIiD0wIUH1CVyoL0ERDmF4H_M2g"  # TODO: jezus don't put your token in the code
        self.channels = {"general": 1286796583463157834, "alerts": 1288673494762000466}
        self.loop = asyncio.new_event_loop()
        self._client_thread: Thread = None

    def send_message(self, message: str) -> None:
        print(f"Sending message: {message}")
        asyncio.run_coroutine_threadsafe(
            self.client.send_message(message, self.channels["general"]), self.loop
        )

    def run(self) -> None:
        self._client_thread = Thread(
            target=self._run_client, name="Discord Client Thread", daemon=True
        )
        self._client_thread.start()

    def _run_client(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.client.start(self.token))
