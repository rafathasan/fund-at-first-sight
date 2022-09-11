import yaml
from pathlib import Path

CONFIG_FILE_PATH = "config/config.yaml"

def parse_config(config_path: str = CONFIG_FILE_PATH):
    return yaml.safe_load(Path(config_path).read_text())