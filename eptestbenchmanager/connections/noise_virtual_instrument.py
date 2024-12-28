import numpy as np

from . import PollingVirtualInstrument


class NoiseVirtualInstrument(PollingVirtualInstrument):
    def __init__(
        self,
        experiment_manager,
        uid: str,
        name: str,
        mean: float,
        standard_deviation: float,
    ):

        self._mean = mean
        self._standard_deviation = standard_deviation
        getter_function = lambda: np.random.normal(self._mean, self._standard_deviation)
        super().__init__(experiment_manager, uid, name, None, None, getter_function, 1000)

    def command(self, command: float) -> None:
        super().command(command)
