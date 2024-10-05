import numpy as np

from . import VirtualInstrument


class NoiseVirtualInstrument(VirtualInstrument):
    def __init__(
        self,
        uid: str,
        name: str,
        mean: float,
        standard_deviation: float,
    ):
        super().__init__(uid, name)
        self._mean = mean
        self._standard_deviation = standard_deviation

    # Override the value property to return a random value from a normal distribution
    @property
    def value(self) -> float:
        return np.random.normal(self._mean, self._standard_deviation)

    def command(self, command: float) -> None:
        super().command(command)
