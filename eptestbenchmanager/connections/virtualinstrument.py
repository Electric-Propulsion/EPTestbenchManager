from typing import Union
from threading import Lock
from abc import ABC, abstractmethod
from functools import partial
from epcomms.equipment.base.instrument import Instrument
from eptestbenchmanager.dashboard.elements import DashboardElement, Graph, Gauge
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
        experiment_manager,
        uid: str,
        name: str,
        rolling_storage_size: int = 250,
    ):
        self._experiment_manager = experiment_manager
        self.uid = uid
        self.name = name
        self.dashboard_elements = {}

        # self.dashboard_element = dashboard_element
        self._value: Union[str, int, float, bool, None] = None
        self._lock = Lock()

        self._rolling_storage = Recording(
            self._experiment_manager,
            f"{self.name}_rolling_storage",
            self.uid,
            max_samples=rolling_storage_size, rolling=True
        )
        # TODO: it would be nice if recordings other than rolling storage could be seen during experiments
        self.add_dashboard_elements( # all virtual instruments by default have a rolling graph and a gauge dashboard elements, corresponding to the rolling storage and the current value of the virtual instrument
            [
                Graph(
                    f"{uid}-rolling-graph",
                    f"{self.name} (Last {rolling_storage_size} Samples)",
                    lambda: self.rolling_storage,
                ),
                Gauge(
                    f"{uid}-gauge",
                    self.name,
                    lambda: self.value,
                )
            ]
            )
        self._rolling_storage.start_recording()
        self._recordings: dict[str, Recording] = {}

    def add_dashboard_elements(
        self, dashboard_element: Union[DashboardElement, list[DashboardElement]]
    ):
        if isinstance(dashboard_element, list):
            for element in dashboard_element:
                self.dashboard_elements[element.uid] = element
                print(f"{element.uid} added tp {self.uid} as a dashboard element")
        else:
            self.dashboard_elements[dashboard_element.uid] = dashboard_element
            print(f"{dashboard_element.uid} added tp {self.uid} as a dashboard element")
        

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
        rolling_storage = self._rolling_storage.record.values
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
        print(f"Getting recording {record_id}: {self._recordings[record_id].record.values}")
        self._lock.acquire()
        record = self._recordings[record_id].record.values
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

    def begin_recording(self, record_id, max_samples=None, stored_samples = 250, max_time=None) -> None:
        """
        Begin a new named recording.
        """
        print(f"Beginning recording {record_id}")
        self._recordings[record_id] = Recording(self._experiment_manager, record_id, self.uid, max_samples, stored_samples, max_time)
        self._recordings[record_id].start_recording()
        self.add_dashboard_elements(
            Graph(
                f"{self.uid}-{record_id}-graph",
                f"{self.name}: {record_id}",
                partial(self.get_recording, record_id)
            )
        )

    def recording_exists(self, record_id) -> bool:
        """
        Check if a recording exists.
        """
        print(f"Checking if {record_id} exists in {self._recordings}")
        return record_id in self._recordings
    
    def resume_recording(self, record_id) -> None:
        """
        Resume a recording.
        """
        print(f"Resuming recording {record_id}")
        self._recordings[record_id].start_recording()

    def stop_recording(self, record_id) -> None:
        """
        Stop a recording.
        """
        print(f"Stopping recording {record_id}")
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
