# Main C2Sketch web application

from c2sketch.app.data import *
from c2sketch.app.config import AppConfig
from c2sketch.app.plugins import AppPluginLoader
from c2sketch.app.model import *
from c2sketch.app.model.manage import manage_models
from c2sketch.app.model.structure import edit_model
from c2sketch.app.execute import *
from c2sketch.app.ui import *
from c2sketch.app.patterns import with_source

from toppyt import (Application, CookieJar, TaskVariable,                 
                    view_information, write_information, sequence_tasks, with_information)

from functools import partial

# Choose a mission plan and main task
def c2sketch_main(config: AppConfig, model_store: ModelStore, execution_store: ExecutionStore, plugin_loader: AppPluginLoader, path_var: TaskVariable, cookie_jar: CookieJar):
     
    def select_task(path: str):
        match path.split('/')[1:]:
            case ['']:
                return sequence_tasks(
                    write_information(path_var,lambda pv: pv.write('/model')),
                    manage_models(config, model_store, path_var, cookie_jar)
                )
            case ['model']:
                return manage_models(config, model_store, path_var, cookie_jar)
            case ['model',model_id]:
                return edit_model(config, model_store, plugin_loader, model_id, path_var, cookie_jar)
            case ['model',model_id,node_type,node_id]:
                return edit_node(config,model_store, plugin_loader, model_id, node_type, node_id, path_var, cookie_jar)
            case ['execute']:
                return manage_executions(config, model_store, execution_store, path_var, cookie_jar)
            case ['execute',scenario_id,'actor',actor_id]:
                return execute_scenario(config, model_store, execution_store, plugin_loader, scenario_id, actor_id, path_var, cookie_jar)
            case ['public-display',display_name]:
                return view_public_display(model_store, execution_store, plugin_loader, display_name)
            case [main_task,*_]:
                return view_information(f'Unknown view {main_task}')    
       
    return with_source(execution_store,with_information(path_var,lambda pv:pv.read(),lambda path: select_task(path)))
       
def c2sketch_page(config: AppConfig, plugin_js_assets:list[str], plugin_css_assets:list[str], task='', session=''):
    
    plugin_js = "\n".join([f'<script src="{js}" defer></script>' for js in plugin_js_assets])
    plugin_css = "\n".join([f'<link rel="stylesheet" href="{css}"/>' for css in plugin_css_assets])
    
    return f'''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>{config.name}</title>
                          
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css" />
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.2/css/bulma.min.css" />
                
                <link rel="stylesheet" href="/static/c2sketch.css" />
                {plugin_css}
                <script src="/static/toppyt.js" defer></script>
                <script src="/static/resizer.js" defer></script>
                <script src="/static/svg-canvas.js" defer></script>
                <script src="/static/c2s_editor.js" type="module"></script>
                {plugin_js}      
            </head>
            <body>
            {session}
            {task}
            </body>
        </html>
        '''

class C2SApp(Application):

    plugin_loader: AppPluginLoader
    model_store: ModelStore
    execution_store: ExecutionStore

    def __init__(self, config: AppConfig):

        self.plugin_loader = AppPluginLoader()

        #Load default plugins
        for plugin in ['data_table','data_transfer','map_plot','timer']:
            self.plugin_loader.load_module(f'c2sketch.plugins.{plugin}')
        
        #Load additional local plugins
        self.plugin_loader.load_from_directory(config.plugin_path)

        #Create data access stores
        self.model_store = ModelStore(model_path = config.model_path, initial_models = self.plugin_loader.models)
        self.model_store.load_model_folder()
        
        self.execution_store = ExecutionStore(model_path= config.model_path, scenario_path=config.scenario_path, plugin_loader=self.plugin_loader)

        plugin_js_assets, plugin_css_assets = self.plugin_loader.plugin_assets()
        
        static_assets = static_assets = [
            'c2sketch.app.static:c2sketch.css',
            'c2sketch.app.static:c2s-logo.png',
            'c2sketch.app.static:resizer.js',
            'c2sketch.app.static:c2s_editor.js',
            'c2sketch.app.static:c2s_mode.js',
            'static']
        plugin_assets = config.plugin_path.joinpath('static')
        if plugin_assets.is_dir():
                static_assets.append(str(plugin_assets))
  
        super().__init__(
            main_task = partial(c2sketch_main, config, self.model_store, self.execution_store, self.plugin_loader),
            layout = partial(c2sketch_page,config,plugin_js_assets,plugin_css_assets),
            static_assets=static_assets
        )

# Main application factory following ASGI conventions
def app(config = AppConfig()):
    return C2SApp(config)