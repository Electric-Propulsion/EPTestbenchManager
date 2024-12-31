from threading import Semaphore, Thread
from . import VirtualInstrument


class CompositeVirtualInstrument(VirtualInstrument):
    def __init__(
        self,
        testbench_manager,
        uid: str,
        name: str,
        composition_function: callable,
        instruments: list[VirtualInstrument],
        unit: str = None,
    ) -> None:
        super().__init__(testbench_manager, uid, name, unit)
        self._instruments = instruments
        self._composition_function = composition_function
        self.update_semaphore = Semaphore(0)
        self._update_thread = Thread(
            target=self._updating_loop, name=f"{self.name} Updating Thread", daemon=True
        )

        for instrument in self._instruments:
            instrument.register_dependant_composite(self)

    def _updating_loop(self) -> None:
        while True:
            self.update_semaphore.acquire()
            new_value = self._composition_function(
            [instrument.value for instrument in self._instruments]
            )
            self._set_value(new_value)
            
    def start_updating(self) -> None:
        self._update_thread.start()

    def command(self, command: float) -> None:
        super().command(command)
