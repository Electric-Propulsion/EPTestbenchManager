from threading import Thread, Semaphore
from typing import Union
from . import VirtualInstrument


class BatchedPollingVirtualInstrument(VirtualInstrument):

    def __init__(
        self,
        testbench_manager,
        uid,
        name,
        setter_function,
        unit=None,
    ):
        super().__init__(testbench_manager, uid, name, unit)

        self._setter_function = setter_function
        
    def command(self, command: Union[str, int, float, bool]) -> None:
        """Command the instrument with a value.

        Args:
            command (Union[str, int, float, bool]): The value to command.
        """
        if self._setter_function is not None:
            self._setter_function(command)
        else:
            super().command(command)

    def set_value(self, value):
        self._set_value(value)
