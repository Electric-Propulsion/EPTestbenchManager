from typing import Union
import logging
from .communication_engine import CommunicationEngine

logger = logging.getLogger(__name__)

class StdoutEngine(CommunicationEngine):
    """A communication engine that outputs messages to the standard output."""

    def __init__(self, alert_manager):
        """Initializes the StdoutEngine with an alert manager."""
        super().__init__(alert_manager)

    def send_message(self, message: str, severity: str, target: Union[str, list[str], None] = None) -> None:
        """Sends a message to the standard output."""
        print(f"{self._format_severity(severity)} {self._format_target(target)} {message}")  # Output the message to standard output

    
    def _format_severity(self, severity: str) -> str:
        """Formats the severity level for display."""
        return f"[{severity.upper()}]"
    
    def _format_target(self, target: Union[str, list[str], None]) -> str:
        """Formats the target for display."""
        if isinstance(target, list):
            target_str = ", ".join(target)
        else:
            target_str = target if target else "No Target"

        return f"(@{target_str})"
    
    def send_file(self, file_path: str, severity: str) -> None:
        """Sends a file to the standard output."""
        print(f"{self._format_severity(severity)} Sending file: {file_path}")
        #Let's be honest, the above is clearly just for debug.
    
    @property
    def operators(self) -> list[str]:
        """Returns a list of operator string identifiers."""
        return ["stdout"]
    
    def configure(self, config):
        """Configures the engine with the provided settings."""
        # No specific configuration needed for stdout engine.
        pass
    
    def run(self) -> None:
        """Runs the engine."""
        logger.debug("StdoutEngine is running...")
        # This is a placeholder for any initialization or setup code needed for the engine.
        # No specific implementation needed for stdout engine.
