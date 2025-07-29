import click
import os, pathlib

from c2sketch.read.folder import model_set_from_folder
from c2sketch.read.model import C2SSyntaxError

from c2sketch.visualizations.task_hierarchy import svg_task_hierarchy

#Examples:
#c2s check ~/my_models_folder namespace.test_model -> check a specific model with dependencies
#c2s check ~/my_models_folder -> check all models in a model set

#Operations:
# - check: read/parse the model(s) and do basic checks: references, constraints, types
# - visualize task-hierarchy
#   visualize actor-network
# -

@click.group()
def cli():
    ...

def validate_model_id(ctx,param,value):
    if value is None:
        return None
    model_folder = ctx.params['model_folder']
    model_filename = f'{value.replace(".",os.sep)}.c2s'
    model_path = pathlib.Path(model_folder).joinpath(model_filename)
    if not model_path.exists():
        raise click.BadParameter(f'Model {value} ({model_filename}) does not exist in folder {model_folder}')
    
    return value

@cli.command()
@click.argument('model_folder', type=click.Path(exists=True,file_okay=False,dir_okay=True))
@click.argument('model_id', type=click.STRING, callback=validate_model_id, required=False)

def check(model_folder, model_id):
    try:
        #Check all models in the folder
        if model_id is None:
            click.echo(f'Reading all models from folder {model_folder}...')
            models = model_set_from_folder(model_folder)
        else:
            click.echo(f'Reading required models for {model_id} from folder {model_folder}...')
            models = model_set_from_folder(model_folder, model_id)
        
        for id, model in models.models.items():
            click.echo(f'Checking {id}...')
            #TODO: Check references
            #TODO: Check types
            #TODO: Check constraints

    except C2SSyntaxError as error:
        click.secho(f'Syntax error: {error.msg}',fg='red')

@cli.group('visualize')
def visualize():
    ...

@visualize.command('task-hierarchy')
@click.argument('model_folder', type=click.Path(exists=True,file_okay=False,dir_okay=True))
@click.argument('model_id', type=click.STRING, callback=validate_model_id, required=True)
def visualize_task_hierarchy(model_folder: str,model_id: str):
    models = model_set_from_folder(model_folder, model_id)
    svg_content = svg_task_hierarchy(models, model_id)
    file_name = f'{model_id.replace(".","-")}.svg'
    pathlib.Path(file_name).write_text(svg_content)
    
if __name__ == '__main__':
    cli()