
from dataclasses import dataclass
import pathlib
import tomli

@dataclass
class AppConfig:
    name = 'C2Sketch'
    host = '127.0.0.1'
    port = 8400
    plugin_path = pathlib.Path('plugins')
    model_path = pathlib.Path('data/models')
    scenario_path = pathlib.Path('data/scenarios')

def read_config(path: pathlib.Path):
    
    config = AppConfig()
    if path.exists():
        with path.open('rb') as f:
            toml = tomli.load(f)
            if 'app_name' in toml:
                config.name = toml['app_name']
    return config