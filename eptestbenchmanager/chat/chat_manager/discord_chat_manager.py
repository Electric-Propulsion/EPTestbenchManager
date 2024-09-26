from . import ChatManager


class DiscordChatManager(ChatManager):
    def configure(self) -> None:
        self._engine.configure_message_processor(self.process_message)

    def process_message(self, message: str) -> None:
        print("running")
        print(self._engine)
        try:
            pass  # self._engine.send_message("Hello from DiscordChatManager")
        except Exception as e:
            print(f"Error processing message: {e}")
        print("done running")
