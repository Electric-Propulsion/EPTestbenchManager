from typing import Union
from threading import Lock
from abc import ABC, abstractmethod
from epcomms.equipment.base.instrument import Instrument


class VirtualInstrument(ABC):
    """
    VirtualInstrument is an abstract base class representing a virtual instrument.
    Attributes:
        uid (str): Unique identifier for the virtual instrument.
        name (str): Name of the virtual instrument.
        _physical_instrument (Instrument): The physical instrument associated with this virtual instrument.
        _setter_function (Union[callable, None]): A function to set the value of the instrument, assumed to be threadsafe.
        _value (Union[str, int, float, bool, None]): The current value of the instrument.
        _lock (Lock): A threading lock to ensure thread safety when accessing or modifying the value.
    Methods:
        value: Property to get the current value of the instrument in a thread-safe manner.
        _set_value(value: Union[str, int, float, bool]): Sets the value of the instrument in a thread-safe manner.
        command(command: Union[str, int, float, bool]): Abstract method to send a command to the instrument. Must be implemented by subclasses.
    """

    def __init__(  # pylint: disable=too-many-arguments #(This is built by a factory)
        self,
        uid: str,
        name: str,
        # dashboard_element: Union[DashboardElement, None], #TODO: Implement DashboardElement #pylint: disable=fixme
    ):
        self.uid = uid
        self.name = name

        # self.dashboard_element = dashboard_element
        self._value: Union[str, int, float, bool, None] = None
        self._lock = Lock()

    @property
    def value(self) -> Union[str, int, float, bool]:
        """
        Retrieve the current value of the virtual instrument.
        This method acquires a lock to ensure thread safety, retrieves the
        value stored in the `_value` attribute, and then releases the lock.
        Returns:
            The current value of the virtual instrument.
        """
        self._lock.acquire()
        value = self._value
        self._lock.release()
        return value

    def _set_value(self, value: Union[str, int, float, bool]) -> None:
        self._lock.acquire()
        self._value = value
        self._lock.release()

    @abstractmethod
    def command(self, command: Union[str, int, float, bool]) -> None:
        """
        Sends a command to the virtual instrument.
        Parameters:
        command (Union[str, int, float, bool]): The command to be sent to the instrument.
            This can be a string, integer, float, or boolean value.
        Raises:
        NotImplementedError: Always raised to indicate that the instrument does not accept commands.
        """
        raise NotImplementedError(
            f"{self.name} (type: {self.__class__.__name__}, uid: {self.uid}) does not accept commands"
        )
