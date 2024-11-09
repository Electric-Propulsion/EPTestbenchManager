from typing import Union
from threading import Lock
from abc import ABC, abstractmethod
from epcomms.equipment.base.instrument import Instrument
from eptestbenchmanager.dashboard.elements import DashboardElement
from eptestbenchmanager.recording import Recording


class VirtualInstrument(ABC):
    """
    VirtualInstrument is an abstract base class representing a virtual instrument.
    Attributes:
        uid (str): Unique identifier for the virtual instrument.
        name (str): Name of the virtual instrument.
        rolling_storage_size (int): The number of values to store in the rolling storage.
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
        rolling_storage_size: int = 250,
    ):
        self.uid = uid
        self.name = name
        self.dashboard_elements = []

        # self.dashboard_element = dashboard_element
        self._value: Union[str, int, float, bool, None] = None
        self._lock = Lock()

        self._rolling_storage = Recording(
            f"{self.name}_rolling_storage",
            max_samples=rolling_storage_size, rolling=True
        )
        self._rolling_storage.start_recording()
        self._recordings: dict[str, Recording] = {}

    def add_dashboard_elements(
        self, dashboard_element: Union[DashboardElement, list[DashboardElement]]
    ):
        if isinstance(dashboard_element, list):
            for element in dashboard_element:
                self.dashboard_elements.append(element)
        else:
            self.dashboard_elements.append(dashboard_element)

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

    @property
    def rolling_storage(self) -> list[Union[str, int, float, bool]]:
        """
        Retrieve the rolling storage of the virtual instrument.
        This method acquires a lock to ensure thread safety, retrieves the
        value stored in the `_rolling_storage` attribute, and then releases the lock.
        Returns:
            The rolling storage of the virtual instrument.
        """
        self._lock.acquire()
        rolling_storage = self._rolling_storage.record.all
        self._lock.release()
        return rolling_storage

    @property
    def rolling_storage_display(self) -> list[Union[str, int, float, bool]]:
        """
        Retrieve the rolling storage of the virtual instrument.
        This method acquires a lock to ensure thread safety, retrieves the
        value stored in the `_rolling_storage` attribute, and then releases the lock.
        Returns:
            The rolling storage of the virtual instrument.
        """
        self._lock.acquire()
        rolling_storage = self._rolling_storage.record.display
        self._lock.release()
        return rolling_storage

    def get_recording(self, record_id: str) -> list[Union[str, int, float, bool]]:
        """
        Retrieve a specific recording by its ID.
        This method acquires a lock to ensure thread safety, retrieves the
        recording from the `_recordings` attribute, and then releases the lock.
        Parameters:
            record_id (str): The ID of the recording to retrieve.
        Returns:
            The recording associated with the given ID, or None if not found.
        """
        print("Attempting to get recording")
        self._lock.acquire()
        record = self._recordings[record_id].record.all
        self._lock.release()
        return record

    def get_recording_display(
        self, record_id: str
    ) -> list[Union[str, int, float, bool]]:
        """
        Retrieve a specific recording by its ID.
        This method acquires a lock to ensure thread safety, retrieves the
        recording from the `_recordings` attribute, and then releases the lock.
        Parameters:
            record_id (str): The ID of the recording to retrieve.
        Returns:
            The recording associated with the given ID, or None if not found.
        """
        self._lock.acquire()
        record = self._recordings[record_id].record.display
        self._lock.release()
        return record

    def _set_value(self, value: Union[str, int, float, bool]) -> None:
        self._lock.acquire()

        self._value = value

        # Update the rolling storage (which should always be active)
        self._rolling_storage.add_sample(value)

        # Update any active recordings
        for recording in self._recordings.values():
            if recording.active:
                recording.add_sample(value)

        self._lock.release()

    def begin_recording(self, record_id, max_samples=None, max_time=None) -> None:
        """
        Begin a new named recording.
        """
        self._recordings[record_id] = Recording(record_id, max_samples, max_time)
        self._recordings[record_id].start_recording()

    def stop_recording(self, record_id) -> None:
        """
        Stop a recording.
        """
        self._recordings[record_id].stop_recording()

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
