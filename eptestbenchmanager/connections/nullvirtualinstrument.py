import logging
from . import VirtualInstrument

logger = logging.getLogger(__name__)


class NullVirtualInstrument(VirtualInstrument):
    """Just a black hole to send commands to ."""

    def __init__(self, testbench_manager, uid: str, name: str, unit: str = None):
        """Initializes the NullVirtualInstrument.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the instrument.
            name (str): Name of the instrument.
            unit (str, optional): Unit of the instrument value. Defaults to None.
        """
        super().__init__(testbench_manager, uid, name, unit)
        self._value = None

    def command(self, command) -> None:
        logger.debug(
            "NullVirtualInstrument %s (%s) received command: %s",
            self.name,
            self.uid,
            command,
        )
