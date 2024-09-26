from typing import Union
from . import AlertManager, AlertSeverity

class DiscordAlertManager(AlertManager):

    def send_alert(self, message: str, severity: AlertSeverity, target: Union[str, list[str], None] = None) -> None:
        if target is not None:
            if isinstance(target, int):
                target_str = f"<@{target}>"
            else:
                target_str = " ".join([f"<@{user}>" for user in target])
        else:
            target_str = ""


        match severity:
            case AlertSeverity.INFO:
                channel = "bot"
                prefix = ":information_source:"
            case AlertSeverity.CAUTION:
                channel = "bot"
                prefix = ":warning:"
            case AlertSeverity.WARNING:
                channel = "general"
                prefix = ":bangbang:"
            case _:
                channel = "bot"
                prefix = ":grey_question:"

        composed_message = f"{prefix} {target_str}\n{message}"

                
        self._engine.send_message(composed_message, channel)