from . import VirtualInstrument


class CompositeVirtualInstrument(VirtualInstrument):
    def __init__(
        self,
        uid: str,
        name: str,
        composition_function: callable,
        instruments: list[VirtualInstrument],
    ) -> None:
        super().__init__(uid, name)
        self._instruments = instruments
        self._composition_function = composition_function

    @property
    def value(self) -> float:
        return self._composition_function(
            [instrument.value for instrument in self._instruments]
        )

    def command(self, command: float) -> None:
        super().command(command)
