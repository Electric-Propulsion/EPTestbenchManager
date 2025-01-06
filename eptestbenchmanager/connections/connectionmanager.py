from pathlib import Path
from os.path import join
from yaml import load, FullLoader
from typing import Union
import epcomms.equipment
import sys
from . import (
    VirtualInstrumentFactory,
    PollingVirtualInstrument,
    ExperimentStatusVirtualInstrument,
    CompositeVirtualInstrument,
)


class ConnectionManager:
    """Manages connections to physical and virtual instruments for the testbench.

    Attributes:
        _physical_instruments (dict): Dictionary of physical instruments.
        _virtual_instruments (dict): Dictionary of virtual instruments.
        _experiment_manager: The experiment manager from the testbench manager.
        _testbench_manager: Global TestbenchManager object.
    """

    def __init__(self, testbench_manager, config_file_path: Union[Path, None] = None):
        """Initializes the ConnectionManager with the given testbench manager and config file path.

        Args:
            testbench_manager: The testbench manager.
            config_file_path (Union[Path, None], optional): Path to the configuration file. Defaults to None.
        """
        self._physical_instruments = {}
        self._virtual_instruments = {}
        self._experiment_manager = testbench_manager.runner
        self._testbench_manager = testbench_manager

        print(
            f"Connection manager config file path: {config_file_path}"
        )  # TODO: make this a logging call

        if config_file_path is not None:
            self.new_apparatus_config(config_file_path)

    def new_apparatus_config(self, config_file_path: Path) -> None:
        """Loads and configures physical and virtual instruments from a given configuration file.

        Args:
            config_file_path (Path): The path to the configuration file.
        """
        config_file_path = Path(config_file_path)
        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config = load(config_file, Loader=FullLoader)

        try:
            for uid, instrument_config in config["physical_instruments"].items():
                module_name = ".".join(instrument_config["class"].split(".")[0:-1])
                class_name = instrument_config["class"].split(".")[-1]
                physical_instrument_class = getattr(
                    sys.modules[module_name], class_name
                )

                self._physical_instruments[uid] = physical_instrument_class(
                    **instrument_config["arguments"]
                )
        except AttributeError as e:
            print(
                f"Error loading physical instruments: {e} (Perhaps none are defined?)"
            )

        for uid, instrument_config in config["virtual_instruments"].items():
            self._virtual_instruments[uid] = VirtualInstrumentFactory.create_instrument(
                self._testbench_manager,
                self._physical_instruments,
                self.virtual_instruments,
                uid,
                instrument_config,
            )

        for virtual_instrument in self._virtual_instruments.values():
            setattr(self, virtual_instrument.uid, virtual_instrument)

        # Virtual instruments that inform about experiment status are hard-coded; they are not defined in the config file
        self._virtual_instruments["experiment_current_segment_id"] = (
            ExperimentStatusVirtualInstrument(
                self._testbench_manager,
                "experiment_current_segment_id",
                "Current Experiment Segment ID",
            )
        )
        self._virtual_instruments["experiment_current_segment_uid"] = (
            ExperimentStatusVirtualInstrument(
                self._testbench_manager,
                "experiment_current_segment_uid",
                "Current Experiment Segment UID",
            )
        )
        self._virtual_instruments["experiment_current_segment_name"] = (
            ExperimentStatusVirtualInstrument(
                self._testbench_manager,
                "experiment_current_segment_name",
                "Current Experiment Segment Name",
            )
        )

    def run(self):
        """Starts polling and updating for virtual instruments."""
        for instrument in self._virtual_instruments.values():
            if isinstance(instrument, PollingVirtualInstrument):
                instrument.start_poll()
            if isinstance(instrument, CompositeVirtualInstrument):
                instrument.start_updating()

    @property
    def virtual_instruments(self):
        """Returns the dictionary of virtual instruments.

        Returns:
            dict: The dictionary of virtual instruments.
        """
        return self._virtual_instruments
