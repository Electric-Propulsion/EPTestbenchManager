from . import ChatManager


class DiscordChatManager(ChatManager):
    """Manages Discord chat interactions for the testbench manager.

    This class handles the configuration of the message processor, processes incoming messages,
    and executes commands sent over discord.

    #TODO: Probably most of this stuff isn't discord-specific, and should be refactored,
    but it works and it's low priority. And we're unlikely to have other chat interfaces in the near
    future.
    """

    def __init__(self, engine, testbench_manager):
        """Initializes the DiscordChatManager with the provided communication engine and testbench manager.

                Args:
                    engine (CommunicationEngine): The discord engine to use for sending messages.
                    testbench_manager (TestbenchManager): Global testbench manager instance.
        .
        """
        super().__init__(engine, testbench_manager)
        self.command_character = "/"

    def configure(self) -> None:
        """Configures the message processor for Discord chat.

        Sets the command character and assigns the message processing function.
        """
        self._engine.configure_message_processor(self.process_message)

    def process_message(self, message: str, channel: str, user: int) -> None:
        """Processes an incoming message and executes the corresponding command.

        Args:
            message (str): The incoming message text.
            channel (str): The channel where the message was sent.
            user (int): The ID of the user who sent the message.

        Returns:
            None
        """
        print(f"responding to {message}")
        try:
            command = next(
                word for word in message.split() if word[0] == self.command_character
            )[1:]
        except StopIteration:
            return  # there was no valid command
        data = message[(len(command) + 1) :].strip()

        mention_string = f"<@{user}>\n"

        match command:
            case "read":
                response = self.query_instrument(data.split()[0])
            case _:
                response = f"{command} is not a valid command"

        try:
            self._engine.send_message(f"{mention_string}{response}", channel)
        except Exception as e:
            print(f"Error processing message: {e}")

    def query_instrument(self, virtual_instrument: str) -> str:
        """Queries a virtual instrument for its current reading.

        Args:
            virtual_instrument (str): The name of the virtual instrument to query.

        Returns:
            str: The reading of the virtual instrument or an error message if the instrument doed
            not exist.
        """
        try:
            instrument = self.testbench_manager.connection_manager.virtual_instruments[
                virtual_instrument
            ]
        except KeyError as e:
            response = f"No such instrument ({virtual_instrument}) exists."
            print(e)
        else:
            response = f"{instrument.name} reports a reading of {instrument.value}"

        return response
