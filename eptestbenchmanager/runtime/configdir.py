from pathlib import Path
from os import path
import logging

from .config import Config

logger = logging.getLogger(__name__)


class ConfigDir(dict):
    """Manages a directory of configuration files."""

    def __init__(self, config_dir: Path):
        """Initializes the ConfigDir with a directory path."""
        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=False)
        self.config_dir = config_dir
        super().__init__()
        self.load_configs()

    def load_configs(self) -> None:
        """Loads all configuration files in the directory."""
        self.clear()
        config_ids = [
            f.stem
            for f in self.config_dir.iterdir()
            if f.is_file() and f.suffix == ".yaml"
        ]

        for config_id in config_ids:
            config_path = Path(path.join(self.config_dir, config_id + ".yaml"))
            try:
                config = Config(config_path)
                self[config_id] = config
            except Exception as e:
                logger.error("Error loading config %s: %s", config_id, e)
                self[config_id] = None  # Store None for failed loads to avoid reloading
