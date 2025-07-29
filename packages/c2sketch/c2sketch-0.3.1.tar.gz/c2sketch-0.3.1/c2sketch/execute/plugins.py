import importlib.util
import inspect
import os

from typing import Any
from pathlib import Path

from c2sketch.models import *

__all__ = ('PluginLoader','Agent')

class Agent:
    """Objects that automate actor behavior"""
    title: str | None
    description: str | None
    actor_id: ActorID | None

    def start(self, time: int, actor_id: ActorID, models: ModelSet) -> None:
        self.actor_id = actor_id
       
    def interact(self, time: int, models: ModelSet) -> list[ScenarioEvent]:
        return []

    def stop(self, time: int) -> None:
        self.actor_id = None

class PluginLoader:

    models: dict[str,Model]
    agents: dict[str,type[Agent]]

    def __init__(self):
        self.models = {}
        self.agents = {}
     
    def load_from_directory(self, plugin_path: str | Path):
        
        if isinstance(plugin_path,str):
            plugin_path = Path(plugin_path)

        if not plugin_path.is_dir():
            return
            
        for folder, _, filenames in plugin_path.walk():
            relative_folder = folder.relative_to(plugin_path)
            if str(relative_folder) == '.':
                for filename in filenames:
                    if filename.endswith('.py'):
                        item_path = folder.joinpath(filename)
                        plugin_module_name = item_path.stem
                        plugin_spec = importlib.util.spec_from_file_location(plugin_module_name, item_path)
                        self._load(plugin_module_name,plugin_spec)
                        
            else:
                plugin_base = str(relative_folder).replace(os.sep,'.')
                for filename in filenames:
                    if filename.endswith('.py'):
                        item_path = folder.joinpath(filename)
                        plugin_module_name = f'{plugin_base}.{item_path.stem}'
                        plugin_spec = importlib.util.spec_from_file_location(plugin_module_name, item_path)
                        self._load(plugin_module_name,plugin_spec)

    def load_module(self, module_name: str):
        self._load(module_name,importlib.util.find_spec(module_name))

    def _load(self, plugin_module_name: str, plugin_spec):
            plugin_module = importlib.util.module_from_spec(plugin_spec)
            plugin_spec.loader.exec_module(plugin_module)
            for plugin_name, plugin_def in inspect.getmembers(plugin_module,self._match_member):
                self._add_member(f'{plugin_module_name}.{plugin_name}', plugin_def)
                
    @staticmethod
    def _match_member(member: Any) -> bool:
        return isinstance(member,Model) or (inspect.isclass(member) and issubclass(member,Agent))
    
    def _add_member(self, plugin_id: str, member: Any):
        if isinstance(member,Model):
            self.models[plugin_id] = member
        elif (inspect.isclass(member) and issubclass(member,Agent)):
            self.agents[plugin_id] = member
