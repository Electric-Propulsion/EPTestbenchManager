from typing import Union
from threading import Lock
from abc import ABC, abstractmethod
from functools import partial
from epcomms.equipment.base.instrument import Instrument
from eptestbenchmanager.recording import Recording

from eptestbenchmanager.dashboard.elements import DigitalGauge
from eptestbenchmanager.dashboard.pages import InstrumentDetail


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
    """

    def __init__(  # pylint: disable=too-many-arguments #(This is built by a factory)
        self,
        testbench_manager,
        uid: str,
        name: str,
        unit: str = None,
        rolling_storage_size: int = 250,
    ):
        """
        Initializes a VirtualInstrument instance.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the virtual instrument.
            name (str): Name of the virtual instrument.
            unit (str, optional): Unit of measurement for the instrument. Defaults to None.
            rolling_storage_size (int, optional): The number of values to store in the rolling storage. Defaults to 250.
        """
        self._experiment_manager = testbench_manager.runner
        self.testbench_manager = testbench_manager
        self.uid = uid
        self.name = name
        self.unit = unit

        self._value: Union[str, int, float, bool, None] = None
        self._lock = Lock()

        self._dependant_composites: list["CompositeVirtualInstrument"] = []

        self._rolling_storage = Recording(
            self.testbench_manager,
            "rolling",
            "Rolling",
            self,
            max_samples=rolling_storage_size,
            rolling=True,
        )
        self._rolling_storage.start_recording()
        self._recordings: dict[str, Recording] = {}

        # Attach the UI elements
        self.gauge = self.testbench_manager.dashboard.create_element(
            DigitalGauge, (self.uid, self.name, self.uid, self.unit)
        )
        self.detail_page = self.testbench_manager.dashboard.create_page(
            InstrumentDetail, (self, self.testbench_manager)
        )

    @property
    def value(self) -> Union[str, int, float, bool]:
        """
        Retrieve the current value of the virtual instrument.

        This method acquires a lock to ensure thread safety, retrieves the value stored in the `_value` attribute,
        and then releases the lock.

        Returns:
            Union[str, int, float, bool]: The current value of the virtual instrument.
        """
        self._lock.acquire()
        value = self._value
        self._lock.release()
        return value

    @property
    def rolling_storage(self) -> Recording:
        """
        Retrieve the rolling storage of the virtual instrument.

        Returns:
            Recording: The rolling storage of the virtual instrument.
        """
        return self._rolling_storage

    def _set_value(self, value: Union[str, int, float, bool]) -> None:
        """
        Set the value of the virtual instrument.

        This method acquires a lock to ensure thread safety, sets the value stored in the `_value` attribute,
        and then releases the lock. It also updates dependant composites, rolling storage, active recordings,
        and the UI gauge component.

        Args:
            value (Union[str, int, float, bool]): The value to set.
        """
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
            self.gauge.set_value(value)
        except RuntimeError as e:
            print(
                f"Error updating gauge for {self.name}: {e}"
            )  # expected until the dashboard is up and running

    def begin_recording(
        self,
        record_id,
        record_name,
        file_id,
        max_samples=None,
        stored_samples=250,
        max_time=None,
    ) -> None:
        """
        Begin a new named recording.

        Args:
            record_id: The ID of the recording.
            record_name: The name of the recording.
            file_id: The file ID for the recording.
            max_samples (optional): The maximum number of samples for the recording. Defaults to None.
            stored_samples (optional): The number of samples to store. Defaults to 250.
            max_time (optional): The maximum time for the recording. Defaults to None.
        """
        print(f"Beginning recording {record_id}")
        self._recordings[record_id] = Recording(
            self.testbench_manager,
            record_id,
            record_name,
            self,
            max_samples,
            stored_samples,
            max_time,
            file_id=file_id,
        )
        self._recordings[record_id].start_recording()
        self.detail_page.update_graphs()

    def recording_exists(self, record_id) -> bool:
        """
        Check if a recording exists.

        Args:
            record_id: The ID of the recording to check.

        Returns:
            bool: True if the recording exists, False otherwise.
        """
        print(f"Checking if {record_id} exists in {self._recordings}")
        return record_id in self._recordings

    def resume_recording(self, record_id) -> None:
        """
        Resume a recording.

        Args:
            record_id: The ID of the recording to resume.
        """
        print(f"Resuming recording {record_id}")
        self._recordings[record_id].start_recording()

    def stop_recording(self, record_id) -> None:
        """
        Stop a recording.

        Args:
            record_id: The ID of the recording to stop.
        """
        print(f"Stopping recording {record_id}")
        self._recordings[record_id].stop_recording()

    def register_dependant_composite(
        self, composite: "CompositeVirtualInstrument"
    ) -> None:
        """
        Register a composite virtual instrument as a dependant of this virtual instrument.

        Args:
            composite (CompositeVirtualInstrument): The composite virtual instrument to register.
        """
        self._dependant_composites.append(composite)

    @abstractmethod
    def command(self, command: Union[str, int, float, bool]) -> None:
        """
        Sends a command to the virtual instrument.

        Args:
            command (Union[str, int, float, bool]): The command to be sent to the instrument. This can be a string, integer, float, or boolean value.

        Raises:
            NotImplementedError: Always raised to indicate that the instrument does not accept commands.
        """
        raise NotImplementedError(
            f"{self.name} (type: {self.__class__.__name__}, uid: {self.uid}) does not accept commands"
        )
