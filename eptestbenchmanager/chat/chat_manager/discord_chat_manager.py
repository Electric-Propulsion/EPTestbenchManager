from . import ChatManager


class DiscordChatManager(ChatManager):
    def configure(self) -> None:
        self._engine.configure(self.process_message)

    def process_message(self, message: str) -> None:
        print("running")
        print(self._engine)
        try:
            self._engine.send_message("Hello from DiscordChatManager")
        except Exception as e:
            print(f"Error processing message: {e}")
        print("done running")
