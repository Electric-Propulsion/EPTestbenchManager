from typing import Union
from epcomms.equipment.base.instrument import Instrument
from . import VirtualInstrument

class CommandDrivenVirtualInstrument(VirtualInstrument):
    """Assumed not to change value spontaneously, but only when commanded."""

    def __init__(
        self,
        testbench_manager,
        uid: str,
        name: str,
        physical_instrument: Instrument,
        setter_function: callable,  # We assume this is threadsafe
        getter_function: callable,  # We assume this is threadsafe
        unit: str = None,
    ):
        """Initializes the CommandDrivenVirtualInstrument.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the instrument.
            name (str): Name of the instrument.
            physical_instrument (Instrument): The physical instrument being polled.
            setter_function (callable): Function to set the instrument value.
            getter_function (callable): Function to get the instrument value.
            unit (str, optional): Unit of the instrument value. Defaults to None.
        """
        super().__init__(testbench_manager, uid, name, unit)
        self._physical_instrument = physical_instrument
        self._setter_function = setter_function
        self._getter_function = getter_function


    def command(self, command: Union[str, int, float, bool]) -> None:
        self._setter_function(command)
        value = self._getter_function()
        self._set_value(value)