from pathlib import Path
from os.path import join
from yaml import load, FullLoader
from typing import Union
import epcomms.equipment
import sys
from . import VirtualInstrumentFactory, PollingVirtualInstrument


class ConnectionManager:

    def __init__(self, experiment_manager, config_file_path: Union[Path, None] = None):

        self._physical_instruments = {}
        self._virtual_instruments = {}
        self._experiment_manager = experiment_manager

        print(
            f"Connection manager config file path: {config_file_path}"
        )  # TODO: make this a logging call

        if config_file_path is not None:
            self.new_apparatus_config(config_file_path)

    def new_apparatus_config(self, config_file_path: Path) -> None:
        """
        Loads and configures physical and virtual instruments from a given configuration file.
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
                self._experiment_manager,
                self._physical_instruments,
                self.virtual_instruments,
                uid,
                instrument_config,
            )

        for virtual_instrument in self._virtual_instruments.values():
            setattr(self, virtual_instrument.uid, virtual_instrument)

    def run(self):  # TODO: fix this? Make things more accessible?
        print("********** RUNNING POLLS **********")
        print(self._virtual_instruments.values())
        for instrument in self._virtual_instruments.values():
            if isinstance(instrument, PollingVirtualInstrument):
                print(f"**** STARTING POLL {instrument.uid}")
                instrument.start_poll()

    @property
    def virtual_instruments(self):
        return self._virtual_instruments
