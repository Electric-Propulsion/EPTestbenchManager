from typing import Union
from . import AlertManager, AlertSeverity


class DiscordAlertManager(AlertManager):

    def send_alert(
        self,
        message: str,
        severity: AlertSeverity,
        target: Union[str, list[str], None] = None,
    ) -> None:
        if target is not None:
            try:
                if isinstance(target, str):
                    target_str = f"<@{self._engine._user_ids[target]}>"
                else:
                    target_str = " ".join(
                        [f"<@{self._engine._user_ids[user]}>" for user in target]
                    )
            except KeyError:
                print(f"Failed to send alert to {target} (not in known users).")
                target_str = ""
        else:
            target_str = ""

        prefix = self.get_prefix(severity)
        channel = self.get_channel(severity)

        composed_message = f"{prefix} {target_str}\n{message}"

        self._engine.send_message(composed_message, channel)


    def send_file(
        self,
        file_path: str,
        severity: AlertSeverity,
    ) -> None:
        
        channel = self.get_channel(severity)

        self._engine.send_file(file_path, channel)


    def get_prefix(self, severity: str) -> AlertSeverity:
        match severity:
            case AlertSeverity.INFO:
                return ":information_source:"
            case AlertSeverity.CAUTION:
                return ":warning:"
            case AlertSeverity.WARNING:
                return ":bangbang:"
            case _:
                return ":grey_question:"
            
    def get_channel(self, severity: str) -> str:
        match severity:
            case "info":
                return "bot"
            case "caution":
                return "bot"
            case "warning":
                return "general"
            case _:
                return "bot"
