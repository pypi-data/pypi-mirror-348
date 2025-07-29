
from typing import Callable, Optional, Any
from dataclasses import dataclass

from toppyt import DataSource

from c2sketch.models import *
from c2sketch.execute import PluginLoader
import inspect

@dataclass
class InformationSpaceGraphic:
    title: str | None  = None
    description: str | None = None
    ifs_id: InformationSpaceID | None = None

    def start(self, time: int, ifs_id: InformationSpaceID, models: ModelSet):
        """Configure the plugin"""
        self.ifs_id = ifs_id

    def render_svg(self, time: int, records: list[Record]) -> str:
        """Render the content of the information space"""
        return "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"800\" height=\"600\"></svg>"

@dataclass
class InformationSpaceUI:
    """Visualization plugin to display and manipulate information spaces"""
    title: str
    description: str
    config_type: Optional[RecordType]
    control_ui: Callable[[Optional[DataSource],Optional[DataSource],Optional[RecordType],Optional[Record]],Task]
    js_requirements: Optional[list[str]] = None
    css_requirements: Optional[list[str]] = None

class AppPluginLoader(PluginLoader):
    """Extension of plugin loader that also loads visualization plugins"""

    info_space_uis: dict[str,InformationSpaceUI]
    info_space_graphics: dict[str,type[InformationSpaceGraphic]]

    def __init__(self):
        super().__init__()
        self.info_space_uis = {}
        self.info_space_graphics = {}

    @staticmethod
    def _match_member(member: Any) -> bool:
        return isinstance(member,InformationSpaceUI) or\
            inspect.isclass(member) and issubclass(member,InformationSpaceGraphic) or\
            PluginLoader._match_member(member)
    
    def _add_member(self, plugin_id: str, member: Any):
        super()._add_member(plugin_id, member)
        
        if isinstance(member,InformationSpaceUI):
            self.info_space_uis[plugin_id] = member
        if inspect.isclass(member) and issubclass(member,InformationSpaceGraphic):
            self.info_space_graphics[plugin_id] = member
        
    def plugin_assets(self) -> tuple[list[str],list[str]]:
        all_js = []
        all_css = []
        for viz in self.info_space_uis.values():
            if viz.js_requirements is not None:
                all_js.extend([r for r in viz.js_requirements if r not in all_js])
            if viz.css_requirements is not None:
                all_css.extend([r for r in viz.js_requirements if r not in all_css])
        
        return (all_js, all_css)