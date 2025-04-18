import logging
import discord

logger = logging.getLogger(__name__)


class DiscordClient(discord.Client):
    """A Discord client for handling messages and sending responses.

    Attributes:
        process_message (callable): A function to process incoming messages.
    """

    def __init__(self, *args, **kwargs):
        """Initializes the DiscordClient with optional arguments.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        """Called when the client is ready and connected to Discord."""
        logger.info("Logged in as %s (ID: %s)", self.user, self.user.id)

    async def send_message(self, message: str, channel: int) -> None:
        """Sends a message to a specified channel.

        Args:
            message (str): The message to send.
            channel (int): The ID of the channel to send the message to.
        """
        try:
            channel = self.get_channel(channel)
            await channel.send(message)
        except Exception as e:
            logger.warning("Error sending message: %s", e)

    async def send_file(self, file_path: str, channel: int) -> None:
        """Sends a file to a specified channel.

        Args:
            file_path (str): The path to the file to send.
            channel (int): The ID of the channel to send the file to.
        """
        try:
            channel = self.get_channel(channel)
            await channel.send(file=discord.File(file_path))
        except Exception as e:
            logger.warning("Error sending file: %s", e)
