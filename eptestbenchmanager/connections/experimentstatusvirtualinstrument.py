from . import VirtualInstrument


class ExperimentStatusVirtualInstrument(VirtualInstrument):
    """A virtual instrument for monitoring experiment status.

    This class inherits from VirtualInstrument and is used to monitor the status of experiments.
    It does not support sending commands.
    """

    def set_value(self, value):
        """Sets the value of the instrument. This method is used to update the experiment status.

        Args:
            value: The value to be set.
        """
        self._set_value(value)

    def command(self, command):
        """Raises NotImplementedError as this instrument does not support commands.

        Args:
            command (str): The command to be sent to the instrument.

        Raises:
            NotImplementedError: Always raised as this instrument does not support commands.
        """
        raise NotImplementedError(
            "ExperimentStatusVirtualInstrument does not support commands"
        )
