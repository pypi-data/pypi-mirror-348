"""Read a collection of models from a folder of files"""

from ..models.identifier import ModelID
from ..models.collection import ModelSet

from .model import model_from_c2s_file

import pathlib, os

def model_set_from_folder(path: str | pathlib.Path, required_for_model: ModelID | None = None, allow_syntax_errors: bool = False) -> ModelSet:
    models = ModelSet()

    if isinstance(path,str):
        path = pathlib.Path(path)

    if required_for_model is None:
        #Simpy read all c2s files from a folder
        for folder, _, filenames in path.walk():
            relative_folder = folder.relative_to(path)
            if str(relative_folder) == '.':
                for filename in filenames:
                    if filename.endswith('.c2s'):
                        model_path = folder.joinpath(filename)
                        model_id = model_path.stem
                        models.add_model(model_from_c2s_file(model_id, model_path, allow_syntax_errors))
            else:
                model_base = str(relative_folder).replace(os.sep,'.')
                for filename in filenames:
                    if filename.endswith('.c2s'):
                        model_path = folder.joinpath(filename)
                        model_id = f'{model_base}.{model_path.stem}'
                        models.add_model(model_from_c2s_file(model_id, model_path, allow_syntax_errors))

    else:
        #Read only models while imports require them
        required = [required_for_model]
        while required:
            model_id = required.pop(0)
            model_path = path.joinpath(f'{model_id.replace('.',os.sep)}.c2s')
            if model_path.exists():
                model = model_from_c2s_file(model_id, model_path, allow_syntax_errors)
                models.add_model(model)
                for model_import in model.imports:
                    if model_import.reference not in required and not models.model_exists(model_import.reference):
                        required.append(model_import.reference)
        
    return models

def list_models_in_folder(path: str | pathlib.Path) -> set[ModelID]:
    if isinstance(path,str):
        path = pathlib.Path(path)

    model_ids = set()
    for folder, _, filenames in path.walk():
        relative_folder = folder.relative_to(path)
        if str(relative_folder) == '.':
            for filename in filenames:
                if filename.endswith('.c2s'):
                    model_path = folder.joinpath(filename)
                    model_ids.add(model_path.stem)
        else:
            model_base = str(relative_folder).replace(os.sep,'.')
            for filename in filenames:
                if filename.endswith('.c2s'):
                    model_path = folder.joinpath(filename)
                    model_ids.add(f'{model_base}.{model_path.stem}')  
    return model_ids