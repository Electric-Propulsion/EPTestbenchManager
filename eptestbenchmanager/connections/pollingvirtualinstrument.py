from typing import Union
from threading import Thread, Event
from time import monotonic, sleep
from epcomms.equipment.base.instrument import Instrument
from . import VirtualInstrument


class PollingVirtualInstrument(VirtualInstrument):
    """A virtual instrument that polls a physical instrument at regular intervals.

    Attributes:
        _physical_instrument (Instrument): The physical instrument being polled.
        _setter_function (Union[callable, None]): Function to command the physical instrument with a
        value.
        _getter_function (Union[callable, None]): Function to get the physical instrument value.
        _polling_interval (int): Interval between polls in milliseconds.
        _polling_thread (Thread): Thread that runs the polling loop.
        _stop_event (Event): Event to signal the polling thread to stop.
    """

    def __init__(  # pylint: disable=too-many-arguments #(This is built by a factory)
        self,
        testbench_manager,
        uid: str,
        name: str,
        physical_instrument: Instrument,
        setter_function: Union[callable, None],  # We assume this is threadsafe
        getter_function: Union[callable, None],  # We assume this is threadsafe
        polling_interval: int,  # in milliseconds
        unit: str = None,
    ):
        """Initializes the PollingVirtualInstrument.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the instrument.
            name (str): Name of the instrument.
            physical_instrument (Instrument): The physical instrument being polled.
            setter_function (Union[callable, None]): Function to set the instrument value.
            getter_function (Union[callable, None]): Function to get the instrument value.
            polling_interval (int): Interval between polls in milliseconds.
            unit (str, optional): Unit of the instrument value. Defaults to None.
        """
        super().__init__(testbench_manager, uid, name, unit)
        self._physical_instrument = physical_instrument
        self._setter_function = setter_function
        self._getter_function = getter_function
        self._polling_interval = polling_interval
        self._polling_thread = Thread(
            target=self._polling_loop, name=f"{self.name} Polling Thread", daemon=True
        )
        self._stop_event = Event()

    def command(self, command: Union[str, int, float, bool]) -> None:
        """Command the instrument with a value.

        Args:
            command (Union[str, int, float, bool]): The value to command.
        """
        if self._setter_function is not None:
            self._setter_function(command)
        else:
            super().command(command)

    def start_poll(self) -> None:
        """Starts the polling thread."""
        self._stop_event.clear()
        self._polling_thread.start()

    def halt_poll(self) -> None:
        """Stops the polling thread."""
        self._stop_event.set()

    def _polling_loop(self) -> None:
        """The main polling loop that runs in a separate thread."""
        while True:
            next_poll_time = monotonic() + self._polling_interval / 1000
            if self._stop_event.is_set():
                return  # Exit the thread
            try:
                value = self._getter_function()
                self._set_value(value)
            except Exception as e:
                print(f"Instrument {self.name} encountered exception: {e}")
            sleep_time = next_poll_time - monotonic()
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                # We missed the polling interval
                print(
                    f"EPTestbenchManager: Instrument {self.name} missed a polling interval by {-sleep_time} seconds."
                )
                pass
