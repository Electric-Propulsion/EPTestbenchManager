from pathlib import Path
import yaml


class Config(dict):
    """Configuration class that extends the built-in dictionary."""

    def __init__(self, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Configuration file {path} does not exist.")
        if not path.is_file():
            raise IsADirectoryError(f"Configuration file {path} is not a file.")
        if not path.suffix == ".yaml":
            raise ValueError(f"Configuration file {path} is not a YAML file.")

        config_dict = self._load_yaml(path)
        super().__init__(config_dict)
        self.path = path

    def _load_yaml(self, path: Path) -> dict:
        """Loads a YAML file and returns its content as a dictionary."""
        with open(path, "r", encoding="utf-8") as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ValueError(f"Error loading config YAML file {path}: {e}") from e
