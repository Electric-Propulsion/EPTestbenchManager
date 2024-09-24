from epcomms.equipment.base.instrument import Instrument
from . import VirtualInstrument, PollingVirtualInstrument


class VirtualInstrumentFactory:

    @classmethod
    def create_instrument(
        cls, physical_instruments: list[Instrument], uid: str, config: dict
    ) -> VirtualInstrument:
        """
        Create a virtual instrument from a configuration dictionary.
        Args:
            config (dict): A dictionary containing the configuration for the virtual instrument.
        Returns:
            VirtualInstrument: A virtual instrument object.
        """
        if config["type"] == "polling":
            return cls._create_polling_instrument(physical_instruments, uid, config)
        else:
            raise ValueError(f"Invalid virtual instrument type: {config['type']}")

    @classmethod
    def _create_polling_instrument(
        cls, physical_instruments: list[Instrument], uid: str, config: dict
    ) -> PollingVirtualInstrument:
        """
        Create a polling virtual instrument from a configuration dictionary.
        Args:
            config (dict): A dictionary containing the configuration for the virtual instrument.
        Returns:
            PollingVirtualInstrument: A polling virtual instrument object.
        """

        physical_instrument = physical_instruments[config["physical_instrument"]]

        setter_function = (
            getattr(physical_instrument, config["setter_function"])
            if config["setter_function"]
            else None
        )

        getter_function = (
            getattr(physical_instrument, config["getter_function"])
            if config["getter_function"]
            else None
        )

        return PollingVirtualInstrument(
            uid=uid,
            name=config["name"],
            physical_instrument=physical_instrument,
            setter_function=setter_function,
            getter_function=getter_function,
            polling_interval=config["polling_interval"],
        )
