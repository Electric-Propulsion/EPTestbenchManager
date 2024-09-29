from . import ChatManager


class DiscordChatManager(ChatManager):
    def configure(self) -> None:
        self._engine.configure_message_processor(self.process_message)
        self.command_character = '/'

    def process_message(self, message: str, channel: str, user: int) -> None:
        print(f"responding to {message}")
        try:
            command = next(word for word in message.split() if word[0] == self.command_character)[1:]
        except StopIteration:
            return # there was no valid command
        data = message[(len(command)+1):].strip()

        mention_string = f"<@{user}>\n"

        match command:
            case 'read':
                response = self.query_instrument(data.split()[0])
            case 'run':
                response = self.begin_experiment(data.split()[0])
            case _:
                response = f"{command} is not a valid command"

        try:
            self._engine.send_message(f"{mention_string}{response}", channel)
        except Exception as e:
            print(f"Error processing message: {e}")

    def query_instrument(self, virtual_instrument: str) -> str:
        try:
            instrument = self.testbench_manager.connection_manager.virtual_instruments[virtual_instrument]
        except KeyError as e:
            response = f"No such instrument ({virtual_instrument}) exists."
            print(e)
        else:
            response = f"{instrument.name} reports a reading of {instrument.value}"

        return response
    
    def begin_experiment(self, experiment: str) -> str:
        try:
            self.testbench_manager.runner.run_experiment(experiment)
            return f"Now running {experiment}"
        except KeyError as e:
            print(e)
            return f"No such experiment ({experiment}) exists."

    
