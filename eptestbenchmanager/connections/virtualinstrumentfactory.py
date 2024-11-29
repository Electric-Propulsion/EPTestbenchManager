import numpy as np
from epcomms.equipment.base.instrument import Instrument
from eptestbenchmanager.dashboard.elements import DashboardElement, Graph, Gauge
from . import (
    VirtualInstrument,
    PollingVirtualInstrument,
    NoiseVirtualInstrument,
    CompositeVirtualInstrument,
)


class VirtualInstrumentFactory:

    @classmethod
    def create_instrument(
        cls,
        experiment_manager,
        physical_instruments: list[Instrument],
        virtual_instruments: list[VirtualInstrument],
        uid: str,
        config: dict,
    ) -> VirtualInstrument:
        """
        Create a virtual instrument from a configuration dictionary.
        Args:
            config (dict): A dictionary containing the configuration for the virtual instrument.
        Returns:
            VirtualInstrument: A virtual instrument object.
        """
        match config["type"]:
            case "polling":
                return cls._create_polling_instrument(experiment_manager, physical_instruments, uid, config)
            case "noise":
                return cls._create_noise_instrument(experiment_manager, uid, config)
            case "composite":
                print(virtual_instruments)
                return cls._create_composite_instrument(
                    experiment_manager, virtual_instruments, uid, config
                )
            case _:
                raise ValueError(f"Invalid virtual instrument type: {config['type']}")

    @classmethod
    def _create_polling_instrument(
        cls, experiment_manager, physical_instruments: list[Instrument], uid: str, config: dict
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
            if config["setter_function"] != "None"
            else None
        )

        getter_function = (
            getattr(physical_instrument, config["getter_function"])
            if config["getter_function"] != "None"
            else None
        )

        return PollingVirtualInstrument(
            experiment_manager,
            uid=uid,
            name=config["name"],
            physical_instrument=physical_instrument,
            setter_function=setter_function,
            getter_function=getter_function,
            polling_interval=config["polling_interval"],
        )

    @classmethod
    def _create_noise_instrument(cls, experiment_manager, uid: str, config: dict) -> NoiseVirtualInstrument:
        """
        Create a noise virtual instrument from a configuration dictionary.
        Args:
            config (dict): A dictionary containing the configuration for the virtual instrument.
        Returns:
            NoiseVirtualInstrument: A noise virtual instrument object.
        """
        print("creating noise")
        instrument = NoiseVirtualInstrument(
            experiment_manager,
            uid=uid,
            name=config["name"],
            mean=config["mean"],
            standard_deviation=config["standard_deviation"],
        )
        return instrument

    @classmethod
    def _create_composite_instrument(
        cls, experiment_manager, virtual_instruments: list[Instrument], uid: str, config: dict
    ) -> CompositeVirtualInstrument:
        """
        Create a composite virtual instrument from a configuration dictionary.
        Args:
            config (dict): A dictionary containing the configuration for the virtual instrument.
        Returns:
            CompositeVirtualInstrument: A composite virtual instrument object.
        """
        try:
            instruments = [
                virtual_instruments[instrument] for instrument in config["instruments"]
            ]
        except KeyError as e:
            raise ValueError(
                f"Invalid instrument UID ({e}). Ensure all parent instruments are defined before composite instruments."
            ) from e

        composition_function = cls._get_composition_function(
            config["composition_function"], len(instruments)
        )

        return CompositeVirtualInstrument(
            experiment_manager,
            uid=uid,
            name=config["name"],
            composition_function=composition_function,
            instruments=instruments,
        )

    @classmethod
    def _get_composition_function(cls, function_name: str, num_instruments) -> callable:
        """
        Get the composition function from the function name.
        Args:
            function_name (str): The name of the composition function.
        Returns:
            callable: The composition function.
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
