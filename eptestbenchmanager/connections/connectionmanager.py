from pathlib import Path
from os.path import join
from yaml import load, FullLoader
from typing import Union
import epcomms.equipment
import sys
from . import VirtualInstrumentFactory


class ConnectionManager:

    def __init__(self, config_file_path: Union[Path, None] = None):

        self._physical_instruments = {}
        self._virtual_instruments = {}

        if config_file_path is None:
            # Assume it's in ../config/apparatus_config.yaml
            config_file_path = join(
                Path(__file__).parent.parent, Path("config/apparatus_config.yaml")
            )
            print(config_file_path)  # TODO: make this a logging call

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

            for uid, instrument_config in config["physical_instruments"].items():
                module_name = ".".join(instrument_config["class"].split(".")[0:-1])
                class_name = instrument_config["class"].split(".")[-1]
                physical_instrument_class = getattr(sys.modules[module_name] , class_name)

                self._physical_instruments[uid] = physical_instrument_class(
                    **instrument_config["arguments"]
                )

            for uid, instrument_config in config["virtual_instruments"].items():
                self._virtual_instruments[uid] = (
                    VirtualInstrumentFactory.create_instrument(
                        self._physical_instruments,
                        uid,
                        instrument_config,
                    )
                )

    def run(self): #TODO: fix this? Make things more accessible?
        for instrument in self._virtual_instruments:
            self._virtual_instruments[instrument].start_poll()
            #self._virtual_instruments[instrument]._polling_thread.join()    
        import time
        while(True):
            for instrument in self._virtual_instruments:
                print(self._virtual_instruments[instrument].value)
                time.sleep(0.01)


