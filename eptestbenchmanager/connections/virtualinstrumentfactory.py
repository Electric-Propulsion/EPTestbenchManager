import numpy as np
from epcomms.equipment.base.instrument import Instrument
from . import (
    VirtualInstrument,
    PollingVirtualInstrument,
    NoiseVirtualInstrument,
    CompositeVirtualInstrument,
    ManualVirtualInstrument,
    CommandDrivenVirtualInstrument,
    NullVirtualInstrument,
)


class VirtualInstrumentFactory:
    """Factory class for creating virtual instruments."""

    @classmethod
    def create_instrument(
        cls,
        testbench_manager,
        physical_instruments: list[Instrument],
        virtual_instruments: list[VirtualInstrument],
        uid: str,
        config: dict,
    ) -> VirtualInstrument:
        """Creates a virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            physical_instruments (list[Instrument]): List of physical instruments.
            virtual_instruments (list[VirtualInstrument]): List of virtual instruments.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            VirtualInstrument: A virtual instrument object.

        Raises:
            ValueError: If the virtual instrument type is invalid.
        """
        match config["type"]:
            case "polling":
                return cls._create_polling_instrument(
                    testbench_manager, physical_instruments, uid, config
                )
            case "command_driven":
                return cls.create_command_driven_instrument(
                    testbench_manager, physical_instruments, uid, config
                )
            case "noise":
                return cls._create_noise_instrument(testbench_manager, uid, config)
            case "null":
                return cls.create_null_instrument(testbench_manager, uid, config)
            case "manual":
                return cls.create_manual_instrument(testbench_manager, uid, config)
            case "composite":
                return cls._create_composite_instrument(
                    testbench_manager, virtual_instruments, uid, config
                )
            case _:
                raise ValueError(f"Invalid virtual instrument type: {config['type']}")

    @classmethod
    def _create_polling_instrument(
        cls,
        testbench_manager,
        physical_instruments: list[Instrument],
        uid: str,
        config: dict,
    ) -> PollingVirtualInstrument:
        """Creates a polling virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            physical_instruments (list[Instrument]): List of physical instruments.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            PollingVirtualInstrument: A polling virtual instrument object.
        """
        physical_instrument = physical_instruments[config["physical_instrument"]]

        setter_arguments = config.get("setter_arguments", {})
        setter_function = (
            (
                lambda value: getattr(physical_instrument, config["setter_function"])(
                    value, **setter_arguments
                )
            )
            if config["setter_function"] != "None"
            else None
        )

        getter_arguments = config.get("getter_arguments", {})
        getter_function = (
            (
                lambda: (
                    getattr(physical_instrument, config["getter_function"])(
                        **getter_arguments
                    )
                )
            )
            if config["getter_function"] != "None"
            else None
        )

        return PollingVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            physical_instrument=physical_instrument,
            setter_function=setter_function,
            getter_function=getter_function,
            polling_interval=config["polling_interval"],
            unit=config.get("unit", None),
        )

    @classmethod
    def create_null_instrument(
        cls, testbench_manager, uid: str, config: dict
    ) -> NullVirtualInstrument:
        """Creates a null virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            NullVirtualInstrument: A null virtual instrument object.
        """
        instrument = NullVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            unit=config.get("unit", None),
        )
        return instrument

    @classmethod
    def _create_noise_instrument(
        cls, testbench_manager, uid: str, config: dict
    ) -> NoiseVirtualInstrument:
        """Creates a noise virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            NoiseVirtualInstrument: A noise virtual instrument object.
        """
        instrument = NoiseVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            mean=config["mean"],
            standard_deviation=config["standard_deviation"],
            unit=config.get("unit", None),
        )
        return instrument

    @classmethod
    def create_manual_instrument(
        cls, testbench_manager, uid: str, config: dict
    ) -> ManualVirtualInstrument:
        """Creates a manual virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            ManualVirtualInstrument: A manual virtual instrument object.
        """
        instrument = ManualVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            unit=config.get("unit", None),
        )
        return instrument

    @classmethod
    def create_command_driven_instrument(
        cls,
        testbench_manager,
        physical_instruments: list[Instrument],
        uid: str,
        config: dict,
    ) -> CommandDrivenVirtualInstrument:

        # TODO: This is too similar to the polling instrument creation. Refactor to reduce redundancy.
        physical_instrument = physical_instruments[config["physical_instrument"]]

        setter_arguments = config.get("setter_arguments", {})
        setter_function = (
            (
                lambda value: getattr(physical_instrument, config["setter_function"])(
                    value, **setter_arguments
                )
            )
            if config["setter_function"] != "None"
            else None
        )

        getter_arguments = config.get("getter_arguments", {})
        getter_function = (
            (
                lambda: (
                    getattr(physical_instrument, config["getter_function"])(
                        **getter_arguments
                    )
                )
            )
            if config["getter_function"] != "None"
            else None
        )

        instrument = CommandDrivenVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            physical_instrument=physical_instrument,
            setter_function=setter_function,
            getter_function=getter_function,
            unit=config.get("unit", None),
        )

        return instrument

    @classmethod
    def _create_composite_instrument(
        cls,
        testbench_manager,
        virtual_instruments: list[Instrument],
        uid: str,
        config: dict,
    ) -> CompositeVirtualInstrument:
        """Creates a composite virtual instrument from a configuration dictionary.

        Args:
            testbench_manager: Global TestbenchManager object.
            virtual_instruments (list[Instrument]): List of virtual instruments.
            uid (str): Unique identifier for the virtual instrument.
            config (dict): Configuration dictionary for the virtual instrument.

        Returns:
            CompositeVirtualInstrument: A composite virtual instrument object.

        Raises:
            ValueError: If a parent instrument UID is invalid.
        """
        try:
            instruments = [
                virtual_instruments[instrument] for instrument in config["instruments"]
            ]
        except KeyError as e:
            raise ValueError(
                f"Invalid instrument UID ({e}). Ensure all parent instruments are defined before composite instruments."  # pylint: disable=line-too-long
            ) from e

        composition_function = cls._get_composition_function(
            config["composition_function"], len(instruments)
        )

        return CompositeVirtualInstrument(
            testbench_manager,
            uid=uid,
            name=config["name"],
            composition_function=composition_function,
            instruments=instruments,
            unit=config.get("unit", None),
        )

    @classmethod
    def _get_composition_function(cls, function_name: str, num_instruments) -> callable:
        """Gets the composition function from the function name.

        Args:
            function_name (str): The name of the composition function.
            num_instruments (int): Number of instruments.

        Returns:
            callable: The composition function.

        Raises:
            ValueError: If the composition function is invalid or if 'divide' is used with incorrect
            number of instruments.
        """
        match function_name:
            case "sum":
                return sum
            case "mean":
                return np.mean
            case "median":
                return np.median
            case "max":
                return max
            case "min":
                return min
            case "product":
                return np.prod
            case "divide":
                if num_instruments != 2:
                    raise ValueError(
                        "The 'divide' composition function requires exactly two instruments."
                    )
                return lambda x: x[0] / x[1]
            case _:
                raise ValueError(f"Invalid composition function: {function_name}")
