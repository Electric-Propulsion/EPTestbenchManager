from typing import Union
from eptestbenchmanager.dashboard.elements import SettableDigitalGauge
from . import VirtualInstrument


class ManualVirtualInstrument(VirtualInstrument):
    """
    A virtual instrument that is manually set by the user, via the GUI, rather than being associated
    with a physical instrument."""

    def __init__(self, testbench_manager, uid: str, name: str, unit: str = None):
        self.gauge = testbench_manager.dashboard.create_element(
            SettableDigitalGauge, (uid, name, uid, unit, self)
        )
        super().__init__(testbench_manager, uid, name, unit)
        # Attach the UI elements
        

    def set_value(self, value: Union[str, int, float, bool]) -> None:
        """
        Set the value of the instrument. This is the public method that should be called from
        the GUI, as an interface to the private _set_value() method.

        Args:
            value (Union[str, int, float, bool]): The value to set.
        """

        self._set_value(value)

    def command(self, command: Union[str, int, float, bool]) -> None:
        """Raises NotImplementedError as this instrument does not support commands.

        Args:
            command (str): The command to be sent to the instrument.

        Raises:
            NotImplementedError: Always raised as this instrument does not support commands.
        """
        raise NotImplementedError(
            "ManualVirtualInstrument does not support commands"
        )
        