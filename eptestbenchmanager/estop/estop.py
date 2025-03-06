import yaml
import importlib
import sys
from os import path
from pathlib import Path

from epcomms.equipment.relay import Relay

import logging

logger = logging.getLogger(__name__)

class EStop:
    def __init__(self, config_file_path: Path = Path(path.join(Path(__file__).parent, Path("estop_config.yaml")))):
        try:
            with open(config_file_path, 'r') as file:
                config = yaml.safe_load(file)

            self.enabled = config['enabled']
            module_name = ".".join(config["relay"].split(".")[0:-1])
            importlib.import_module(module_name)
            class_name = config["relay"].split(".")[-1]
            self.relay = getattr(sys.modules[module_name], class_name)(**config["relay_args"])
        
            self.fired = False
            logger.info("EStop initialized with config: %s", config)
        except Exception as e:
            self.enabled = False
            logger.info("Estop disabled (Couldn't initialilze: %s)", e)
            raise e

    
    def estop_fire(self):
        if self.enabled:
            self.relay.set_state(Relay.State.OPEN)
            self.fired = True
            logger.critical("EStop fired")
        else:
            logger.warning("EStop is disabled, ignoring fire request")

    def estop_reset(self, force: bool = False):
        if self.enabled:
            if not self.fired or force:
                self.relay.set_state(Relay.State.CLOSED)
                self.fired = False
                logger.info("EStop reset")
            else:
                logger.warning("Estop already fired, ignoring reset request")
        else:
            logger.warning("EStop is disabled, ignoring reset request")
            



    