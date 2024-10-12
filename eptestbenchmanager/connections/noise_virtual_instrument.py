import numpy as np
from eptestbenchmanager.dashboard.elements import Graph

from . import PollingVirtualInstrument


class NoiseVirtualInstrument(PollingVirtualInstrument):
    def __init__(
        self,
        uid: str,
        name: str,
        mean: float,
        standard_deviation: float,
    ):

        self._mean = mean
        self._standard_deviation = standard_deviation
        getter_function = lambda: np.random.normal(self._mean, self._standard_deviation)
        super().__init__(uid, name, None, None, getter_function, 100)

    def command(self, command: float) -> None:
        super().command(command)
