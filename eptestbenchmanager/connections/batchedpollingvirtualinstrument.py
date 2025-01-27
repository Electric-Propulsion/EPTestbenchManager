from threading import Thread, Semaphore
from typing import Union
from . import VirtualInstrument


class BatchesPollingVirtualInstrument(VirtualInstrument):

    def __init__(
        self,
        testbench_manager,
        uid,
        name,
        batcher,
        setter_function,
        unit=None,
    ):
        super().__init__(testbench_manager, uid, name, unit)

        self._batcher = batcher
        self._setter_function = setter_function

        self._update_thread = Thread(
            target=self._update_loop, name=f"{self.name} Update Thread", daemon=True
        )

        self._update_semaphore = Semaphore(0)

    def command(self, command: Union[str, int, float, bool]) -> None:
        """Command the instrument with a value.

        Args:
            command (Union[str, int, float, bool]): The value to command.
        """
        if self._setter_function is not None:
            self._setter_function(command)
        else:
            super().command(command)

    def update(self):
        self._update_semaphore.release()

    def _update_loop(self):
        while True:
            self._update_semaphore.acquire()

    def start(self):
        self._update_thread = Thread(
            target=self._update_loop, name=f"{self.name} Update Thread", daemon=True
        )
        self._update_thread.start()
