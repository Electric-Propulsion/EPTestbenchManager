import discord


class DiscordClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.process_message = None

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

    def configure_message_processor(self, process_message: callable):
        self.process_message = process_message

    async def on_message(self, message):
        if self.process_message is not None:
            self.process_message(message)

    async def send_message(self, message: str, channel: int) -> None:
        try:
            channel = self.get_channel(channel)
            await channel.send(message)
        except Exception as e:
            print(f"Error sending message: {e}")
