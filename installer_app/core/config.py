# loading configuration from YAML file
import yaml
from typing import Dict, Any


def load_config(path: str = "config.yaml") -> Dict[str, Any]:
    try:
        with open(path) as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{path}' not found.")
