import numpy as np

from . import PollingVirtualInstrument


class NoiseVirtualInstrument(PollingVirtualInstrument):
    def __init__(
        self,
        testbench_manager,
        uid: str,
        name: str,
        mean: float,
        standard_deviation: float,
        unit: str = None,
    ):

        self._mean = mean
        self._standard_deviation = standard_deviation
        getter_function = lambda: np.random.normal(self._mean, self._standard_deviation)
        super().__init__(testbench_manager, uid, name, None, None, getter_function, 1000, unit)

    def command(self, command: float) -> None:
        super().command(command)
