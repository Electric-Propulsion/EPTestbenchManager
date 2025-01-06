from typing import Union
from . import AlertManager, AlertSeverity


class DiscordAlertManager(AlertManager):
    """Manages alerts sent to Discord.

    This class provides methods to send alerts and files to a Discord channel based on the severity
    of the alert. Note that the term 'alert' is used here to refer to any message or file for legacy
    reasons.
    """

    def send_alert(
        self,
        message: str,
        severity: AlertSeverity,
        target: Union[str, list[str], None] = None,
    ) -> None:
        """Sends an alert message to a Discord channel.

        Args:
            message (str): The alert message to send.
            severity (AlertSeverity): The severity level of the alert.
            target (Union[str, list[str], None], optional): The target user(s) to mention.
            Defaults to None.
        """
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
        """Sends a file to a Discord channel.

        Args:
            file_path (str): The path to the file to send.
            severity (AlertSeverity): The severity level of the alert.
        """
        channel = self.get_channel(severity)

        self._engine.send_file(file_path, channel)

    def get_prefix(self, severity: str) -> AlertSeverity:
        """Gets the prefix emoji for a given severity level.

        Args:
            severity (str): The severity level.

        Returns:
            AlertSeverity: The corresponding emoji for the severity level.
        """
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
        """Gets the Discord channel for a given severity level.

        Channels are hardcoded. This method should be updated if the Discord server changes.

        Args:
            severity (str): The severity level.

        Returns:
            str: The corresponding Discord channel for the severity level.
        """
        match severity:
            case "info":
                return "bot"
            case "caution":
                return "bot"
            case "warning":
                return "general"
            case _:
                return "bot"
