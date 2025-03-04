import logging
from threading import Semaphore, Thread, Event
from . import VirtualInstrument

logger = logging.getLogger(__name__)


class CompositeVirtualInstrument(VirtualInstrument):
    """A composite virtual instrument that combines multiple virtual instruments.

    This class allows for the combination of multiple virtual instruments into a single
    composite instrument. The values of the individual instruments are combined using a
    user-defined composition function.

    Attributes:
        testbench_manager: The testbench manager instance.
        uid: The unique identifier for the instrument.
        name: The name of the instrument.
        composition_function: A callable that combines the values of the instruments.
        instruments: A list of VirtualInstrument instances to be combined.
        unit: The unit of measurement for the instrument.
        update_semaphore: A semaphore to control the update loop.
        _update_thread: A thread that runs the update loop.
    """

    def __init__(
        self,
        testbench_manager,
        uid: str,
        name: str,
        composition_function: callable,
        instruments: list[VirtualInstrument],
        unit: str = None,
    ) -> None:
        """Initializes the CompositeVirtualInstrument.

        Args:
            testbench_manager: The testbench manager instance.
            uid: The unique identifier for the instrument.
            name: The name of the instrument.
            composition_function: A callable that combines the values of the instruments.
            instruments: A list of VirtualInstrument instances to be combined.
            unit: The unit of measurement for the instrument. Defaults to None.
        """
        super().__init__(testbench_manager, uid, name, unit)
        self._instruments = instruments
        self._composition_function = composition_function
        self.update_semaphore = Semaphore(0)
        self._update_thread = Thread(
            target=self._updating_loop, name=f"{self.name} Updating Thread", daemon=True
        )
        self._stop_event = Event()

        for instrument in self._instruments:
            instrument.register_dependant_composite(self)

    def _updating_loop(self) -> None:
        """The loop that updates the composite instrument's value.

        This loop runs in a separate thread and updates the value of the composite
        instrument by applying the composition function to the values of the individual
        instruments.
        """
        while True:
            self.update_semaphore.acquire()
            if self._stop_event.is_set():
                return  # Exit the thread
            try:
                new_value = self._composition_function(
                    [instrument.value for instrument in self._instruments]
                )
            except TypeError as e:
                logger.error("Error in composition function for %s: %s", self.name, e)
                new_value = None
            self._set_value(new_value)

    def start_updating(self) -> None:
        """Starts the update loop in a separate thread."""
        self._stop_event.clear()
        try:
            self._update_thread.start()
        except RuntimeError:
            logger.error(f"Instrument {self.name} updating thread already started.")

    def halt_updating_thread(self) -> None:
        """Stops the update loop."""
        self._stop_event.set()
        self.update_semaphore.release()

    def join_updating_thread(self) -> None:
        """Joins the update loop thread."""
        if self._update_thread.is_alive():
            self._update_thread.join()

    def command(self, command: float) -> None:
        """Raises NotImplementedError as this instrument does not support commands.

        Args:
            command (str): The command to be sent to the instrument.

        Raises:
            NotImplementedError: Always raised as this instrument does not support commands.
        """
        raise NotImplementedError(
            "CompositeVirtualInstrument does not support commands"
        )
