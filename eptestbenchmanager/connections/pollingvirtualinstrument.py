from typing import Union
from threading import Lock, Thread, Event
from time import monotonic, sleep
from epcomms.equipment.base.instrument import Instrument, MeasurementError
from . import VirtualInstrument


class PollingVirtualInstrument(VirtualInstrument):

    def __init__(  # pylint: disable=too-many-arguments #(This is built by a factory)
        self,
        experiment_manager,
        uid: str,
        name: str,
        physical_instrument: Instrument,
        setter_function: Union[callable, None],  # We assume this is threadsafe
        getter_function: Union[callable, None],  # We assume this is threadsafe
        polling_interval: int,  # in milliseconds
        # dashboard_element: Union[DashboardElement, None], #TODO: Implement DashboardElement #pylint: disable=fixme
    ):
        super().__init__(experiment_manager, uid, name)
        self._physical_instrument = physical_instrument
        self._setter_function = setter_function
        self._getter_function = getter_function
        self._polling_interval = polling_interval
        self._polling_thread = Thread(
            target=self._polling_loop, name=f"{self.name} Polling Thread", daemon=True
        )
        self._stop_event = Event()

    def command(self, command: Union[str, int, float, bool]) -> None:
        if self._setter_function is not None:
            self._setter_function(command)
        else:
            super().command(command)

    def start_poll(self) -> None:
        self._stop_event.clear()
        self._polling_thread.start()

    def halt_poll(self) -> None:
        self._stop_event.set()

    def _polling_loop(self) -> None:
        while True:
            next_poll_time = monotonic() + self._polling_interval / 1000
            if self._stop_event.is_set():
                return  # Exit the thread
            try:
                value = self._getter_function()
            except MeasurementError:
                value = None
            print(f"{self.uid}: {value}")
            self._set_value(value)
            sleep_time = next_poll_time - monotonic()
            if sleep_time > 0:
                sleep(sleep_time)
            else:
                # We missed the polling interval
                # TODO: Log a warning
                pass
