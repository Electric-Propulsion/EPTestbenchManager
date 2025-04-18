from pathlib import Path
import os
import logging
import platform
from datetime import datetime

from .configdir import ConfigDir

logger = logging.getLogger(__name__)


class RuntimeManager:

    def __init__(self, app_data_dir: Path = None):
        self.configs = {}
        app_data_dir = self.get_base_app_data_dir(app_data_dir)
        if not app_data_dir.exists():
            app_data_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir = app_data_dir / "config"
        if not self.config_dir.exists():
            self.config_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir = app_data_dir / "logs"
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True, exist_ok=True)
        self.secrets_dir = app_data_dir / "secrets"
        if not self.secrets_dir.exists():
            self.secrets_dir.mkdir(parents=True, exist_ok=True)

        # load or create the expected configdirs
        self.configs["experiment_config"] = ConfigDir(
            self.config_dir / "experiment_config"
        )
        self.configs["apparatus_config"] = ConfigDir(
            self.config_dir / "apparatus_config"
        )

    def get_base_app_data_dir(self, app_data_dir: Path = None) -> Path:
        """Returns the base application data directory."""
        if app_data_dir is not None:
            return app_data_dir.expanduser()
        elif "EPTESTBENCH_CONFIG_DIR" in os.environ:
            return Path(os.environ["EPTESTBENCH_APP_DATA_DIR"]).expanduser()
        elif platform.system() == "Windows":
            base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        elif platform.system() == "Linux":
            base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
        elif platform.system() == "Darwin":
            logger.critical("MacOS is not supported.")
            raise NotImplementedError("MacOS is not supported.")
        else:
            logger.critical("Unsupported OS.")
            raise NotImplementedError("Unsupported OS.")

        return base / "eptestbench"

    def configure_logging(self, log_level: str = "INFO"):
        """Configures logging for the application."""
        logfile = os.path.join(
            self.log_dir,
            f'EPTestbenchManager {datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.log',
        )

        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(logfile, "w", "utf-8"),
                logging.StreamHandler(),
            ],
        )

        logger.info("Logging to %s", logfile)
        logger.info("Logging level set to %s", log_level)
