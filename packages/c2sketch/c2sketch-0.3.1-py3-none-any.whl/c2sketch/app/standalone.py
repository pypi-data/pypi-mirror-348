import uvicorn # type: ignore
import click
import pathlib
from c2sketch.app import app
from c2sketch.app.config import read_config

@click.command() 
@click.option('--config_path',type=click.Path(dir_okay=False),default='data/config.toml')
@click.option('--host',type=str)
@click.option('--port',type=int)
@click.option('--plugin_path',type=click.Path(file_okay=False))
@click.option('--model_path',type=click.Path(file_okay=False))
@click.option('--scenario_path',type=click.Path(file_okay=False))
def serve(config_path,host,port,plugin_path,model_path,scenario_path):
    
    config = read_config(pathlib.Path(config_path))
    #CLI options overrule the configuration file

    if host is not None:
        config.host = host
    if port is not None:
        config.port = port
    if plugin_path is not None:
        config.plugin_path = pathlib.Path(plugin_path)
    if model_path is not None:
        config.model_path = pathlib.Path(model_path)
    if scenario_path is not None:
        config.scenario_path = pathlib.Path(scenario_path)

    uvicorn.run(app(config),host=config.host,port=config.port)

if __name__ == '__main__':
    serve()