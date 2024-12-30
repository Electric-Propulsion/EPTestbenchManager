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

    @property
    def value(self) -> float:
        return self._composition_function(
            [instrument.value for instrument in self._instruments]
        )

    def command(self, command: float) -> None:
        super().command(command)
