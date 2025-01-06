import numpy as np

from . import PollingVirtualInstrument


class NoiseVirtualInstrument(PollingVirtualInstrument):
    """A virtual instrument that generates noise based on a normal distribution.

    This class simulates a noise-generating instrument by producing random values from a normal
    distribution with specified mean and standard deviation.

    Attributes:
        _mean (float): The mean value of the normal distribution.
        _standard_deviation (float): The standard deviation of the normal distribution.
    """

    def __init__(
        self,
        testbench_manager,
        uid: str,
        name: str,
        mean: float,
        standard_deviation: float,
        unit: str = None,
    ):
        """Initializes the NoiseVirtualInstrument with the given parameters.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): The unique identifier for the instrument.
            name (str): The name of the instrument.
            mean (float): The mean value of the normal distribution.
            standard_deviation (float): The standard deviation of the normal distribution.
            unit (str, optional): The unit of measurement. Defaults to None.
        """
        self._mean = mean
        self._standard_deviation = standard_deviation
        getter_function = lambda: np.random.normal(self._mean, self._standard_deviation)
        super().__init__(
            testbench_manager, uid, name, None, None, getter_function, 1000, unit
        )

    def command(self, command: float) -> None:
        """Sends a command to the instrument.

        Args:
            command (float): The command value to be sent to the instrument.
        """
        super().command(command)
