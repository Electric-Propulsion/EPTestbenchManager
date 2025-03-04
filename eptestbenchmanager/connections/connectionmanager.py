import logging
from threading import Thread, Lock
from pathlib import Path
import os
import sys
from yaml import load, FullLoader
import importlib
from eptestbenchmanager.dashboard.elements import ApparatusControl

from . import (
    VirtualInstrumentFactory,
    PollingVirtualInstrument,
    ExperimentStatusVirtualInstrument,
    CompositeVirtualInstrument,
    Batcher,
)

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages connections to physical and virtual instruments for the testbench.

    Attributes:
        _physical_instruments (dict): Dictionary of physical instruments.
        _virtual_instruments (dict): Dictionary of virtual instruments.
        _experiment_manager: The experiment manager from the testbench manager.
        _testbench_manager: Global TestbenchManager object.
    """

    def __init__(self, testbench_manager, config_dir: Path):
        """Initializes the ConnectionManager with the given testbench manager and config file path.

        Args:
            testbench_manager: The testbench manager.
            config_file_path (Union[Path, None], optional): Path to the configuration file.
            Defaults to None.
        """
        self._physical_instruments = {}
        self._batchers = {}
        self._virtual_instruments = {}
        self._experiment_manager = testbench_manager.runner
        self._testbench_manager = testbench_manager
        self.current_apparatus_config = None

        logger.info("Initializing ConnectionManager")
        logger.info("Connection manager config file dir: %s", config_dir)
        self.config_dir = config_dir
        self._configs = None
        self.update_apparatus_configs()
        self.ui_element = self._testbench_manager.dashboard.create_element(
            ApparatusControl, ("apparatus_control", self)
        )

        self.reload = None
        self._shutdown_complete = Lock()
        self._shutdown_complete.acquire()

    def register_reload(self, reload_element):
        """Registers a reload element to the connection manager.

        Args:
            reload_element (Reload): The reload element.
        """
        self.reload = reload_element

    def update_apparatus_configs(self) -> list:
        """Returns a list of all apparatus configs on the system.

        Args:
            config_dir (Path): The path to the directory containing configuration files.

        Returns:
            list: List of apparatus configs.
        """
        self._configs = [
            f.stem
            for f in self.config_dir.iterdir()
            if f.is_file() and f.suffix == ".yaml"
        ]

    @property
    def apparatus_configs(self) -> list:
        """Returns a list of all apparatus configs on the system.

        Returns:
            list: List of apparatus configs.
        """
        return self._configs

    def set_apparatus_config(self, apparatus_config: str) -> None:
        """Sets the apparatus configuration to the given configuration.

        Args:
            apparatus_config (str): The apparatus configuration to set.
        """

        set_apparatus_config_thread = Thread(
            target=self._set_apparatus_config, args=(apparatus_config,)
        )

        set_apparatus_config_thread.start()

    def _set_apparatus_config(self, apparatus_config: str) -> None:
        self.current_apparatus_config = None # it's reset as part of the process

        try:
            if apparatus_config not in self._configs:
                logger.error("Invalid apparatus config: %s", apparatus_config)
                return
            print("setting up apparatus config")
            # Signal the shutdown of the current polling threads
            for batcher in self._batchers.values():
                batcher.halt_poll()
            for instrument in self._virtual_instruments.values():
                if isinstance(instrument, PollingVirtualInstrument):
                    instrument.halt_poll()
                if isinstance(instrument, CompositeVirtualInstrument):
                    instrument.halt_updating_thread()

            # Join the polling threads
            for batcher in self._batchers.values():
                batcher.join_poll()
            for instrument in self._virtual_instruments.values():
                if isinstance(instrument, PollingVirtualInstrument):
                    instrument.join_poll()
                if isinstance(instrument, CompositeVirtualInstrument):
                    instrument.join_updating_thread()

            self._virtual_instruments = {}
            self._batchers = {}

            # Close all physical instruments
            for instrument in self._physical_instruments.values():
                try:
                    instrument.close()
                except Exception as e:
                    logger.error("Error closing physical instrument: %s", e)



            # Load the configuration file for the selected apparatus
            config_file_path = os.path.join(self.config_dir, f"{apparatus_config}.yaml")
            self.load_instruments(config_file_path)

            # Start polling and updating for virtual instruments
            self.run()

            # (Re)Load the experiments
            self._testbench_manager.runner.load_experiments()
            self.current_apparatus_config = apparatus_config

        finally:
            # Update the UI with the new apparatus configuration
            # do this if it succeeds or not
            if self.reload is not None:
                self.reload.reload()


    def load_instruments(self, config_file_path: str) -> None:
        """Loads and configures physical and virtual instruments from a given configuration file.

        Args:
            config_file_path (Path): The path to the configuration file.
        """

        # I think what we need to do here is a) close all existing physical instruments, and
        # b) stop all existing polling threads

        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config = load(config_file, Loader=FullLoader)

        try:
            for uid, instrument_config in config["physical_instruments"].items():
                module_name = ".".join(instrument_config["class"].split(".")[0:-1])
                class_name = instrument_config["class"].split(".")[-1]
                importlib.import_module(module_name)
                physical_instrument_class = getattr(
                    sys.modules[module_name], class_name
                )

                self._physical_instruments[uid] = physical_instrument_class(
                    **instrument_config["arguments"]
                )
        except AttributeError as e:
            logger.error(
                "Error loading physical instruments: %s (Perhaps none are defined?)", e
            )

        for uid, instrument_config in config["virtual_instruments"].items():
            self._virtual_instruments[uid] = VirtualInstrumentFactory.create_instrument(
                self._testbench_manager,
                self._physical_instruments,
                self._batchers,
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

        for batcher in self._batchers.values():
            batcher.start_poll()

    @property
    def virtual_instruments(self):
        """Returns the dictionary of virtual instruments.

        Returns:
            dict: The dictionary of virtual instruments.
        """
        return self._virtual_instruments
