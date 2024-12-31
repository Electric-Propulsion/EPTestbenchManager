from typing import Union
from threading import Lock
from abc import ABC, abstractmethod
from functools import partial
from epcomms.equipment.base.instrument import Instrument
from eptestbenchmanager.recording import Recording

from eptestbenchmanager.dashboard.elements import DigitalGauge


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
        testbench_manager,
        uid: str,
        name: str,
        unit: str = None,
        rolling_storage_size: int = 250,
    ):
        self._experiment_manager = testbench_manager.runner
        self.testbench_manager = testbench_manager
        self.uid = uid
        self.name = name
        self.unit = unit

        self._value: Union[str, int, float, bool, None] = None
        self._lock = Lock()

        self._dependant_composites: list["CompositeVirtualInstrument"] = []

        self._rolling_storage = Recording(
            self._experiment_manager,
            f"{self.name}_rolling_storage",
            self.uid,
            max_samples=rolling_storage_size, rolling=True
        )
        self._rolling_storage.start_recording()
        self._recordings: dict[str, Recording] = {}

        # Attach the UI elements
        self._gauge = self.testbench_manager.dashboard.create_element(DigitalGauge, (self.uid, self.name, self.unit))
        


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

        self._lock.release()

        # Update any dependant composite virtual instruments
        for composite in self._dependant_composites:
            composite.update_semaphore.release()
        

        # Update the rolling storage (which should always be active)
        self._rolling_storage.add_sample(value)

        # Update any active recordings
        for recording in self._recordings.values():
            if recording.active:
                recording.add_sample(value)
        try:
            self._gauge.set_value(value)
        except RuntimeError as e:
            print(f"Error updating gauge for {self.name}: {e}") #expected until the dashboard is up and running

    def begin_recording(self, record_id, max_samples=None, stored_samples = 250, max_time=None) -> None:
        """
        Begin a new named recording.
        """
        print(f"Beginning recording {record_id}")
        self._recordings[record_id] = Recording(self._experiment_manager, record_id, self.uid, max_samples, stored_samples, max_time)
        self._recordings[record_id].start_recording()


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

    def register_dependant_composite(self, composite: "CompositeVirtualInstrument") -> None:
        """
        Register a composite virtual instrument as a dependant of this virtual instrument.
        """
        self._dependant_composites.append(composite)

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
