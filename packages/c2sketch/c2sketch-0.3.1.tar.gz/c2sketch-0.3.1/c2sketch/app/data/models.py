
from toppyt import DataSource, read, write


from c2sketch.models import *
from c2sketch.read.folder import model_set_from_folder
from c2sketch.write.model import model_to_c2s_file

from c2sketch.app import edit

from typing import Optional, Any
from pathlib import Path

__all__ = ['ModelStore']

class ModelStore(DataSource):
    """Database abstraction that manages a collection of models"""

    model_path: Path
    model_set: ModelSet
 
    def __init__(self, model_path: Path, initial_models: Optional[dict[str,Model]] = None):
        self.model_path = model_path
        self.model_set = ModelSet()
     
        if initial_models is not None:
            for model_id, model in initial_models.items():
                self.model_set.add_model(model)
             
        super().__init__()

    def load_model_folder(self):
        self.model_set.update(model_set_from_folder(self.model_path,allow_syntax_errors=True))

    def _list_models(self) -> list[ModelID]:
        return list(sorted(self.model_set.list_all_models()))

    def _write_model(self, model_id: ModelID):
        #Write model to disk
        path_segments = model_id.split('.')

        if len(path_segments) > 1:
            namespace_dir = self.model_path.joinpath(*path_segments[:-1])
            
        else:
            namespace_dir = self.model_path
        if not namespace_dir.is_dir():
            namespace_dir.mkdir(parents = True, exist_ok = True)
        
        model = self.model_set.get_model_by_id(model_id)
        model_filename = f'{path_segments[-1]}.c2s'
        model_to_c2s_file(model,namespace_dir.joinpath(model_filename))

    # Managing the set of models
    @read          
    async def list_models(self) -> list[tuple[ModelID, str | None, str | None]]:
        items = []
        for model_id in self.model_set.list_all_models():
            model = self.model_set.get_model_by_id(model_id)
            items.append((model.id,model.title,model.summary))
        return items

    @write
    async def create_model(self, model_id: ModelID, title: str | None = None):
        if self.model_set.model_exists(model_id):
            raise KeyError(f'Model {model_id} already exists')
        model = Model(model_id)
        if title is not None:
            edit.set_attribute(model,'title',title)
        self.model_set.add_model(model)
        self._write_model(model_id)
        
    @write
    async def delete_model(self, model_id: ModelID):
        path_segments = model_id.split('.')
        
        model_filename = f'{path_segments[-1]}.c2s'
        model_path = self.model_path.joinpath(*path_segments[:-1],model_filename)
        if model_path.is_file():
            model_path.unlink()
        
        self.model_set.remove_model(model_id)
     
    ## Editing the elements of a single model ##
    @read
    async def model(self, model_id: ModelID):
        return self.model_set.get_model_by_id(model_id)

    @read
    async def model_complete(self, model_id: ModelID) -> ModelSet:
        return self.model_set

    # Model structure

    @read
    async def actor_exists(self, model_id: ModelID, actor_id: ActorID) -> bool: 
        return self.model_set.actor_exists(actor_id, model_id)

    @read
    async def location_exists(self, model_id: ModelID, location_id: LocationID) -> bool: 
        return self.model_set.location_exists(location_id, model_id)
    
    @read
    async def task_exists(self, model_id: ModelID, task_id: TaskID) -> bool:
        return self.model_set.task_exists(task_id, model_id)
    @read
    async def task_definition_exists(self, model_id: ModelID, task_id: TaskID) -> bool:
        return self.model_set.task_definition_exists(task_id, model_id)
    @read
    async def task_instance_exists(self, model_id: ModelID, task_id: TaskID) -> bool:
        return self.model_set.task_instance_exists(task_id, model_id)
    
    @read
    async def info_space_exists(self, model_id: ModelID, ifs_id: InformationSpaceID) -> bool:
        return self.model_set.info_space_exists(ifs_id, model_id)
    
    @read
    async def record_type_exists(self, model_id: ModelID, type_id: RecordTypeID) -> bool:
        return self.model_set.record_type_exists(type_id, model_id)

    @write
    async def create_actor(self,model_id, actor_name, actor_title = None, actor_description = None, actor_type= None):
        model = self.model_set.get_model_by_id(model_id)
        edit.add_actor(model,actor_name,actor_title,actor_description,actor_type)
        self._write_model(model_id)
    
    @write
    async def create_location(self,model_id, location_name, location_title = None, location_description = None):
        model = self.model_set.get_model_by_id(model_id)
        edit.add_location(model,location_name,location_title,location_description)
        self._write_model(model_id)
    
    @write
    async def create_task(self, model_id, parent_id, task_name, task_title = None, task_description = None):
        if parent_id is not None and parent_id != '':
            parent_node = self.model_set.get_task_by_id(parent_id)
        else:
            parent_node = self.model_set.get_model_by_id(model_id) 
        edit.add_task(parent_node,task_name,task_title,task_description)
        self._write_model(model_id)

    @write
    async def create_task_definition(self, model_id, parent_id, name, type, title = None, description = None):
        if parent_id is not None and parent_id != '':
            parent_node = self.model_set.get_task_by_id(parent_id)
        else:
            parent_node = self.model_set.get_model_by_id(model_id) 
        edit.add_task_definition(parent_node,name,type,title,description)
        self._write_model(model_id)

    @write
    async def create_task_instance(self, model_id, parent_id, name, title = None, description = None):
        if parent_id is not None and parent_id != '':
            parent_node = self.model_set.get_task_by_id(parent_id)
        else:
            parent_node = self.model_set.get_model_by_id(model_id) 
        edit.add_task_instance(parent_node,name,{},title,description)
        self._write_model(model_id)

    @write
    async def create_info_space(self,model_id,ifs_name,ifs_title=None,ifs_description = None,ifs_type= None):
        model = self.model_set.get_model_by_id(model_id)
        edit.add_info_space(model,ifs_name,ifs_title,ifs_description,ifs_type)
        self._write_model(model_id)

    @write
    async def create_record_type(self,model_id,type_name):
        model = self.model_set.get_model_by_id(model_id)
        edit.add_record_type(model,type_name)
        self._write_model(model_id)

    @write
    async def delete_actor(self, model_id, actor_id):
        actor = self.model_set.get_actor_by_id(actor_id,model_id)
        edit.remove_actor(actor)
        self._write_model(model_id)

    @write
    async def delete_location(self, model_id, location_id):
        location = self.model_set.get_location_by_id(location_id,model_id)
        edit.remove_location(location)
        self._write_model(model_id)

    @write
    async def delete_task(self, model_id, task_id):
        task = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_task(task)
        self._write_model(model_id)

    @write
    async def delete_task_definition(self, model_id, task_id):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_task_definition(task_def)
        self._write_model(model_id)
        
    @write
    async def delete_task_instance(self, model_id, task_id):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_task_instance(task_def)
        self._write_model(model_id)

    @write
    async def delete_information_space(self, model_id, ifs_id):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        edit.remove_info_space(ifs)
        self._write_model(model_id)
    
    @write
    async def delete_record_type(self, model_id, type_id):
        type = self.model_set.get_record_type_by_id(type_id,model_id)
        edit.remove_record_type(type)
        self._write_model(model_id)

    # Model node attributes
    @read
    async def model_attributes(self, model_id):
        model = self.model_set.get_model_by_id(model_id)
        return {'name':model.id,'title': model.title, 'summary':model.summary}
    
    @write
    async def write_model_attributes(self, model_id, attributes):
        title = None if attributes is None else attributes['title']
        summary = None if attributes is None else attributes['summary']
        model = self.model_set.get_model_by_id(model_id)
        if title is None or title == '':
            edit.del_attribute(model,'title')
        else:
            edit.set_attribute(model,'title',title)
        if summary is None or summary == '':
            edit.del_attribute(model,'summary')
        else:
            edit.set_attribute(model,'summary',summary)
        
        self._write_model(model_id)

    @read
    async def model_imports(self, model_id):
        model = self.model_set.get_model_by_id(model_id)
        return list(node.reference for node in model.imports)

    @write
    async def model_add_import(self, model_id: ModelID, reference: ModelID):
        model = self.model_set.get_model_by_id(model_id)
        edit.add_import(model,reference)
        self._write_model(model_id)

    @write
    async def model_remove_import(self, model_id: ModelID, reference: ModelID):
        model = self.model_set.get_model_by_id(model_id)
        edit.remove_import(model,reference)
        self._write_model(model_id)

    @read
    async def model_source(self, model_id: ModelID) -> str:
        model = self.model_set.get_model_by_id(model_id)
        return '\n'.join(model.source) if model.source else ''
    
    @read
    async def model_problems(self, model_id: ModelID) -> list[tuple[int,int,str]]:
        model = self.model_set.get_model_by_id(model_id)
        return [(1,1,problem.description) for problem in model.problems]

    @write
    async def write_model_source(self, model_id: ModelID, update: str) -> None:
        model = self.model_set.get_model_by_id(model_id)
        edit.update_node_source(model, update)
        self._write_model(model_id)
    
    # Actor node attributes
    @read
    async def actor_attributes(self, model_id: ModelID, actor_id: ActorID):
        try:
            actor = self.model_set.get_actor_by_id(actor_id, model_id)
        except KeyError:
            return None
    
        return {'name':actor.name,'title':actor.title,'description':actor.description,'type':actor.type}

    @write
    async def write_actor_attributes(self, model_id: ModelID, actor_id: ActorID, attributes: dict[str,str]):
        title = None if attributes is None else attributes['title']
        description = None if attributes is None else attributes['description']
        actor_type = None if attributes is None or attributes['type'] is None else attributes['type']

        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        
        if title is None or title == '':
            edit.del_attribute(actor,'title')
        else:
            edit.set_attribute(actor,'title',title)
        if description is None or description == '':
            edit.del_attribute(actor,'description')
        else:
            edit.set_attribute(actor,'description',description)
        if actor_type is None or actor_type == '':
            edit.del_attribute(actor,'type')
        else:
            edit.set_attribute(actor,'type',actor_type)

        self._write_model(model_id)

    @read
    async def actor_groups(self, model_id: ModelID, actor_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        return actor.groups
    
    @write
    async def actor_create_group(self, model_id: ModelID, actor_id: ActorID, group_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.add_actor_group(actor, group_id)
        self._write_model(model_id)

    @write
    async def actor_delete_group(self, model_id: ModelID, actor_id: ActorID, group_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.remove_actor_group(actor, group_id)
        self._write_model(model_id)

    @read
    async def actor_members(self, model_id: ModelID, actor_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        return actor.members
    
    @write
    async def actor_create_member(self, model_id: ModelID, actor_id: ActorID, member_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.add_actor_member(actor, member_id)
        self._write_model(model_id)

    @write
    async def actor_delete_member(self, model_id: ModelID, actor_id: ActorID, member_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.remove_actor_member(actor, member_id)
        self._write_model(model_id)

    @read
    async def actor_locations(self, model_id: ModelID, actor_id: ActorID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        return actor.locations
    
    @write
    async def actor_create_location(self, model_id: ModelID, actor_id: ActorID, location_id: LocationID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.add_actor_location(actor, location_id)
        self._write_model(model_id)

    @write
    async def actor_delete_location(self, model_id: ModelID, actor_id: ActorID, location_id: LocationID):
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        edit.remove_actor_location(actor, location_id)
        self._write_model(model_id)

    @read
    async def actor_constraints(self, model_id: ModelID, actor_id: ActorID):
        try:
            actor = self.model_set.get_actor_by_id(actor_id, model_id)
        except KeyError:
            return None
    
        return {'for_actor':actor.get_constraint('for-actor'),'at_location':actor.get_constraint('at-location')}
    
    @write
    async def write_actor_constraints(self, model_id: ModelID, actor_id: ActorID, contraints: dict[str,str]):
        for_actor = None if contraints is None else contraints.get('for_actor')
        at_location = None if contraints is None else contraints.get('at_location')

        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        
        if for_actor is None or for_actor == '':
            edit.del_constraint(actor,'for-actor')
        else:
            edit.set_constraint(actor,'for-actor',for_actor)
        if at_location is None or at_location == '':
            edit.del_constraint(actor,'at-location')
        else:
            edit.set_constraint(actor,'at-location',at_location)
      
        self._write_model(model_id)

    @read
    async def actor_source(self, model_id: ModelID, actor_id: ActorID) -> str:
        actor = self.model_set.get_actor_by_id(actor_id, model_id)
        return edit.get_node_source(actor)
    
    @write
    async def write_actor_source(self, model_id: ModelID, actor_id: ActorID, update: str) -> NodeID:
        actor = self.model_set.get_actor_by_id(actor_id, model_id)

        new_node_id = edit.update_node_source(actor,update)
        self._write_model(model_id)
        return new_node_id

    # Location node attributes
    @read
    async def location_attributes(self, model_id, location_id):
        try:
            location = self.model_set.get_location_by_id(location_id, model_id)
        except KeyError:
            return None
        return {'name':location.name,'title':location.title,'description':location.description}

    @write
    async def write_location_attributes(self, model_id: ModelID, location_id: LocationID, attributes: dict[str,str]):
        title = None if attributes is None else attributes['title']
        description = None if attributes is None else attributes['description']
      
        location = self.model_set.get_location_by_id(location_id, model_id)
        
        if title is None or title == '':
            edit.del_attribute(location,'title')
        else:
            edit.set_attribute(location,'title',title)
        if description is None or description == '':
            edit.del_attribute(location,'description')
        else:
            edit.set_attribute(location,'description',description)
       
        self._write_model(model_id)

    @read
    async def location_groups(self, model_id: ModelID, location_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        return location.groups
    
    @write
    async def location_create_group(self, model_id: ModelID, location_id: LocationID, group_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        edit.add_location_group(location, group_id)
        self._write_model(model_id)

    @write
    async def location_delete_group(self, model_id: ModelID, location_id: LocationID, group_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        edit.remove_location_group(location, group_id)
        self._write_model(model_id)

    @read
    async def location_members(self, model_id: ModelID, location_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        return location.members
    
    @write
    async def location_create_member(self, model_id: ModelID, location_id: LocationID, member_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        edit.add_location_member(location, member_id)
        self._write_model(model_id)

    @write
    async def location_delete_member(self, model_id: ModelID, location_id: LocationID, member_id: LocationID):
        location = self.model_set.get_location_by_id(location_id, model_id)
        edit.remove_location_member(location, member_id)
        self._write_model(model_id)

    @read
    async def location_source(self, model_id: ModelID, location_id: LocationID) -> str:
        location = self.model_set.get_location_by_id(location_id, model_id)
        return edit.get_node_source(location)
    
    @write
    async def write_location_source(self, model_id: ModelID, location_id: LocationID, update: str) -> None:
        location = self.model_set.get_location_by_id(location_id, model_id)

        new_node_id = edit.update_node_source(location,update)
        self._write_model(model_id)
        return new_node_id
     
    # Task attributes
    
    @read
    async def task_attributes(self, model_id: ModelID, task_id: TaskID):
        if not self.model_set.task_exists(task_id, model_id):
            return None
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        return {'name':task.name,'title':task.title,'description':task.description,'compound':task.is_compound()}
    
    @write
    async def write_task_attributes(self, model_id: ModelID, task_id: TaskID, general: dict[str,str]):
        title = None if general is None else general.get('title')
        description = None if general is None else general.get('description')
        
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        
        if title is None or title == '':
            edit.del_attribute(task,'title')
        else:
            edit.set_attribute(task,'title',title)
        if description is None or description == '':
            edit.del_attribute(task,'description')
        else:
            edit.set_attribute(task,'description',description)
      
        self._write_model(model_id)

    @read
    async def read_task_triggers(self, model_id: ModelID, task_id: TaskID):
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        return task.triggers
    
    @read
    async def task_info_space_requirements(self, model_id: ModelID, task_id: TaskID):
        task = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        return task.info_space_requirements
        

    @read
    async def task_get_info_req(self, model_id: ModelID, task_id: TaskID, name: str) -> InformationSpaceRequirement:
        task = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        for req in task.info_space_requirements:
            if req.name == name:
                return req
        else:
            raise KeyError()
        
    @write
    async def task_create_info_req(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task = self.model_set.get_task_by_id(task_id, model_id)
        edit.add_info_req(task, name, type, read, write, binding)

    @write
    async def task_update_info_req(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task = self.model_set.get_task_by_id(task_id, model_id)
        edit.update_info_req(task, name, type, read, write, binding)

    @write
    async def task_delete_info_req(self, model_id: ModelID, task_id: TaskID, name: str):
        task = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_info_req(task, name)

    @read
    async def info_spaces_in_scope(self, model_id: ModelID, task_id: TaskID):
        task = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
    
        return list_valid_bindings(self.model_set,task)

    @read
    async def task_for_actor(self, model_id: ModelID, task_id: TaskID):
        task = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        return task.for_actor
    
    @read
    async def task_constraints(self, model_id: ModelID, task_id: TaskID):
        try:
            task = self.model_set.get_task_by_id(task_id, model_id)
        except KeyError:
            return None
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        return {'for_actor':task.get_constraint('for-actor'),'at_location':task.get_constraint('at-location')}
    
    @write
    async def write_task_constraints(self, model_id: ModelID, task_id: TaskID, contraints: dict[str,str]):
        for_actor = None if contraints is None else contraints.get('for_actor')
        at_location = None if contraints is None else contraints.get('at_location')

        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        
        if for_actor is None or for_actor == '':
            edit.del_constraint(task,'for-actor')
        else:
            edit.set_constraint(task,'for-actor',for_actor)
        if at_location is None or at_location == '':
            edit.del_constraint(task,'at-location')
        else:
            edit.set_constraint(task,'at-location',at_location)
      
        self._write_model(model_id)

    @read
    async def task_source(self, model_id: ModelID, task_id: TaskID) -> str:
        if not self.model_set.task_exists(task_id,model_id):
            return ""
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,Task):
            raise ValueError(f'{task_id} does not reference a task')
        
        return edit.get_node_source(task)
   
    @write
    async def write_task_source(self, model_id: ModelID, task_id: TaskID, update: str) -> None:
        task = self.model_set.get_task_by_id(task_id, model_id)
        
        new_node_id = edit.update_node_source(task, update)
        self._write_model(model_id)
        return new_node_id

    # Task definition attributes

    @read
    async def task_def_attributes(self, model_id: ModelID, task_id: TaskID):
        try:
            task_def = self.model_set.get_task_by_id(task_id,model_id)
        except KeyError:
            return None
        
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')

        return {'name':task_def.name,'type':task_def.parameter_type, 'title':task_def.title,'description':task_def.description,'compound':task_def.is_compound()}
    
    @write
    async def write_task_def_attributes(self, model_id: ModelID, task_id: TaskID, attributes: dict[str,str]):
        title = None if attributes is None else attributes.get('title')
        parameter_type = None if attributes is None else attributes.get('type')
        description = None if attributes is None else attributes.get('description')
        
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task')
        
        if title is None or title == '':
            edit.del_attribute(task,'title')
        else:
            edit.set_attribute(task,'title',title)
        if description is None or description == '':
            edit.del_attribute(task,'description')
        else:
            edit.set_attribute(task,'description',description)
      
        if parameter_type is None or parameter_type == '':
            edit.update_task_def_type(task,None)
        else:
            edit.update_task_def_type(task,parameter_type)

        self._write_model(model_id)

    @read
    async def task_def_info_space_requirements(self, model_id: ModelID, task_id: TaskID):
        task_def = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        return task_def.info_space_requirements
        
    @read
    async def task_def_get_info_req(self, model_id: ModelID, task_id: TaskID, name: str) -> InformationSpaceRequirement:
        task_def = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        for req in task_def.info_space_requirements:
            if req.name == name:
                return req
        else:
            raise KeyError()
        
    @write
    async def task_def_create_info_req(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.add_info_req(task_def, name, type, read, write, binding)
        self._write_model(model_id)

    @write
    async def task_def_update_info_req(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.update_info_req(task_def, name, type, read, write, binding)
        self._write_model(model_id)

    @write
    async def task_def_delete_info_req(self, model_id: ModelID, task_id: TaskID, name: str):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_info_req(task_def, name)
        self._write_model(model_id)

    @read
    async def task_def_triggers(self, model_id: ModelID, task_id: TaskID):
        task_def = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        return task_def.triggers
    
    @write
    async def task_def_create_trigger(self, model_id: ModelID, task_id: TaskID, reference: str):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.add_trigger(task_def, reference)
        self._write_model(model_id)

    @write
    async def task_def_delete_trigger(self, model_id: ModelID, task_id: TaskID, name: str):
        task_def = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_trigger(task_def, name)
        self._write_model(model_id)

    @read
    async def task_def_constraints(self, model_id: ModelID, task_id: TaskID):
        try:
            task_def = self.model_set.get_task_by_id(task_id, model_id)
        except KeyError:
            return None
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        return {'for_actor':task_def.get_constraint('for-actor'),'at_location':task_def.get_constraint('at-location')}
    
    @write
    async def write_task_def_constraints(self, model_id: ModelID, task_id: TaskID, contraints: dict[str,str]):
        for_actor = None if contraints is None else contraints.get('for_actor')
        at_location = None if contraints is None else contraints.get('at_location')

        task_def = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        
        if for_actor is None or for_actor == '':
            edit.del_constraint(task_def,'for-actor')
        else:
            edit.set_constraint(task_def,'for-actor',for_actor)
        if at_location is None or at_location == '':
            edit.del_constraint(task_def,'at-location')
        else:
            edit.set_constraint(task_def,'at-location',at_location)
      
        self._write_model(model_id)

    @read
    async def task_def_source(self, model_id: ModelID, task_id: TaskID) -> str:
        task_def = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        
        return edit.get_node_source(task_def)
    
    @write
    async def write_task_def_source(self, model_id: ModelID, task_id: TaskID, update: str) -> None:
        task_def = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_def,TaskDefinition):
            raise ValueError(f'{task_id} does not reference a task definition')
        
        new_node_id = edit.update_node_source(task_def,update)
        self._write_model(model_id)
        return new_node_id

    # Task instance attributes
    @read
    async def task_instance_template_id(self, model_id: ModelID, task_id: TaskID):
        
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        
        return task_instance.get_definition().node_id

    @read
    async def task_instance_attributes(self, model_id: ModelID, task_id: TaskID):
        try:
            task_instance = self.model_set.get_task_by_id(task_id,model_id)
        except KeyError:
            return None
        
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')

        return {'name':task_instance.name,'title':task_instance.get_attribute('title'),'description':task_instance.get_attribute('description')}
    
    @write
    async def write_task_instance_attributes(self, model_id: ModelID, task_id: TaskID, attributes: dict[str,str]):
        title = None if attributes is None else attributes.get('title')
        description = None if attributes is None else attributes.get('description')
        
        task = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task')
        
        if title is None or title == '':
            edit.del_attribute(task,'title')
        else:
            edit.set_attribute(task,'title',title)
        if description is None or description == '':
            edit.del_attribute(task,'description')
        else:
            edit.set_attribute(task,'description',description)

        self._write_model(model_id)

    @read
    async def task_instance_parameter_type(self, model_id: ModelID, task_id: TaskID):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        task_definition = task_instance.get_definition()
 
        if task_definition.parameter_type is None:
            return None
        else:
            try:
                parameter_type = self.model_set.get_record_type_by_id(task_definition.parameter_type, model_id)
            except KeyError:
                parameter_type = None

            return parameter_type
        
    @read
    async def task_instance_parameter(self, model_id: ModelID, task_id: TaskID):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
      
        return task_instance.parameter

    @write
    async def write_task_instance_parameter(self, model_id: ModelID, task_id: TaskID, parameter: dict[str,Any]):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        
        edit.update_task_instance_parameter(task_instance,parameter)
        self._write_model(model_id)

    @read
    async def task_instance_info_space_requirements(self, model_id: ModelID, task_id: TaskID):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        return task_instance.info_space_requirements

    @read
    async def task_instance_info_space_bindings(self, model_id: ModelID, task_id: TaskID):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        return task_instance.info_space_bindings
        
    @read
    async def task_instance_get_info_binding(self, model_id: ModelID, task_id: TaskID, name: str) -> InformationSpaceRequirement:
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task definition')
        for binding in task_instance.info_space_bindings:
            if binding.name == name:
                return binding
        else:
            raise KeyError()
        
    @write
    async def task_instance_create_info_binding(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task_instance = self.model_set.get_task_by_id(task_id, model_id)
        edit.add_info_binding(task_instance, name, binding)

    @write
    async def task_instance_update_info_binding(self, model_id: ModelID, task_id: TaskID, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None):
        task_instance = self.model_set.get_task_by_id(task_id, model_id)
        edit.update_info_binding(task_instance, name, binding)

    @write
    async def task_instance_delete_info_binding(self, model_id: ModelID, task_id: TaskID, name: str):
        task_instance = self.model_set.get_task_by_id(task_id, model_id)
        edit.remove_info_binding(task_instance, name)
    
    @read
    async def task_instance_for_actor(self, model_id: ModelID, task_id: TaskID):
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')

        return task_instance.for_actor
  
    @read
    async def task_instance_constraints(self, model_id: ModelID, task_id: TaskID):
        try:
            task_def = self.model_set.get_task_by_id(task_id, model_id)
        except KeyError:
            return None
        if not isinstance(task_def,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        return {'for_actor':task_def.get_constraint('for-actor'),'at_location':task_def.get_constraint('at-location')}
    
    @write
    async def write_task_instance_constraints(self, model_id: ModelID, task_id: TaskID, contraints: dict[str,str]):
        for_actor = None if contraints is None else contraints.get('for_actor')
        at_location = None if contraints is None else contraints.get('at_location')

        task_instance = self.model_set.get_task_by_id(task_id, model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')
        
        if for_actor is None or for_actor == '':
            edit.del_constraint(task_instance,'for-actor')
        else:
            edit.set_constraint(task_instance,'for-actor',for_actor)
        if at_location is None or at_location == '':
            edit.del_constraint(task_instance,'at-location')
        else:
            edit.set_constraint(task_instance,'at-location',at_location)
      
        self._write_model(model_id)

    @read
    async def task_instance_source(self, model_id: ModelID, task_id: TaskID) -> str:
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')

        return edit.get_node_source(task_instance)
     
    @write
    async def write_task_instance_source(self, model_id: ModelID, task_id: TaskID, update: str) -> None:
        task_instance = self.model_set.get_task_by_id(task_id,model_id)
        if not isinstance(task_instance,TaskInstance):
            raise ValueError(f'{task_id} does not reference a task instance')

        new_node_id = edit.update_node_source(task_instance,update)
        self._write_model(model_id)
        return new_node_id
    
    # Information space attributes
    @read
    async def info_space_attributes(self, model_id: ModelID, ifs_id: InformationSpaceID):
        try:
            ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        except KeyError:
            return None
        ifs_type = None if ifs.type is None else ifs.type
        return {'name':ifs.name,'title':ifs.title,'description':ifs.description,'type':ifs_type}

    @write
    async def write_info_space_attributes(self, model_id: ModelID, ifs_id: InformationSpaceID, attributes: dict[str,str]):
        
        title = None if attributes is None else attributes['title']
        description = None if attributes is None else attributes['description']
        ifs_type = None if attributes is None or attributes['type'] is None else attributes['type']

        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        
        if title is None or title == '':
            edit.del_attribute(ifs,'title')
        else:
            edit.set_attribute(ifs,'title',title)
        if description is None or description == '':
            edit.del_attribute(ifs,'description')
        else:
            edit.set_attribute(ifs,'description',description)
        if ifs_type is None or ifs_type == '':
            edit.update_info_space_type(ifs,None)
        else:
            edit.update_info_space_type(ifs,ifs_type)

        self._write_model(model_id)

    @read
    async def info_space_type(self, model_id: ModelID, ifs_id: InformationSpaceID, dereference = False):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        if ifs.type is not None and dereference:
            return self.model_set.get_record_type_by_id(ifs.type, model_id)
        return ifs.type
        
    @read
    async def info_space_display(self, model_id: ModelID, ifs_id: InformationSpaceID):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return ifs.display
    
    @read
    async def info_space_graphic_type(self, model_id: ModelID, ifs_id: InformationSpaceID):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return ifs.graphic_type
    
    @read
    async def info_space_records(self, model_id: ModelID, ifs_id: InformationSpaceID):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return ifs.records
    
    @read
    async def info_space_get_record(self, model_id: ModelID, ifs_id: InformationSpaceID, sequence_number: int):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        for record in ifs.records:
            if record.sequence_number == sequence_number:
                return record
        else:
            raise KeyError()
       
    @write
    async def info_space_create_record(self, model_id: ModelID, ifs_id: InformationSpaceID, fields: dict[str,str]):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        edit.create_record(ifs,fields)
        self._write_model(model_id)

    @write
    async def info_space_update_record(self, model_id: ModelID, ifs_id: InformationSpaceID, sequence_number: int, fields: dict[str,str]):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        edit.update_record(ifs,sequence_number,fields)
        self._write_model(model_id)

    @write
    async def info_space_delete_record(self, model_id: ModelID, ifs_id: InformationSpaceID, sequence_number: int):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        edit.remove_record(ifs,sequence_number)
        self._write_model(model_id)

    @read
    async def info_space_constraints(self, model_id: ModelID, ifs_id: InformationSpaceID):
        try:
            info_space = self.model_set.get_info_space_by_id(ifs_id, model_id)
        except KeyError:
            return None
        
        return {'for_actor':info_space.get_constraint('for-actor'),'at_location':info_space.get_constraint('at-location')}
    
    @write
    async def write_info_space_constraints(self, model_id: ModelID, ifs_id: InformationSpaceID, contraints: dict[str,str]):
        for_actor = None if contraints is None else contraints.get('for_actor')
        at_location = None if contraints is None else contraints.get('at_location')

        info_space = self.model_set.get_info_space_by_id(ifs_id, model_id)
        
        if for_actor is None or for_actor == '':
            edit.del_constraint(info_space,'for-actor')
        else:
            edit.set_constraint(info_space,'for-actor',for_actor)
        if at_location is None or at_location == '':
            edit.del_constraint(info_space,'at-location')
        else:
            edit.set_constraint(info_space,'at-location',at_location)
      
        self._write_model(model_id)

    @read
    async def info_space_source(self, model_id: ModelID, ifs_id: InformationSpaceID) -> str:
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return edit.get_node_source(ifs)
    
    @write
    async def write_info_space_source(self, model_id: ModelID, ifs_id: InformationSpaceID, update: str) -> None:
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)

        new_node_id = edit.update_node_source(ifs,update)
        self._write_model(model_id)
        return new_node_id
        
    # Record type attributes

    @read
    async def record_type_attributes(self, model_id, type_id):
        try:
            type = self.model_set.get_record_type_by_id(type_id, model_id)
        except KeyError:
            return None
        return {'name':type.name,'title':type.get_attribute('title'),'description':type.get_attribute('description')}

    @write
    async def write_record_type_attributes(self, model_id: ModelID, type_id: RecordTypeID, attributes: dict[str,str]):
        title = None if attributes is None else attributes['title']
        description = None if attributes is None else attributes['description']
      
        type = self.model_set.get_record_type_by_id(type_id, model_id)
        
        if title is None or title == '':
            edit.del_attribute(type,'title')
        else:
            edit.set_attribute(type,'title',title)
        if description is None or description == '':
            edit.del_attribute(type,'description')
        else:
            edit.set_attribute(type,'description',description)
       
        self._write_model(model_id)

    @read
    async def record_type_fields(self, model_id: ModelID, type_id: RecordTypeID):
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        return record_type.fields

    @read
    async def record_type_get_field(self, model_id: ModelID, type_id: RecordTypeID, name: str) -> RecordTypeField:
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        
        for field in record_type.fields:
            if field.name == name:
                return field
        else:
            raise KeyError()
        
    @write
    async def record_type_create_field(self, model_id: ModelID, type_id: RecordTypeID, name: str, type: str):
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        edit.add_field(record_type, name, type)
        self._write_model(model_id)

    @write
    async def record_type_update_field(self, model_id: ModelID, type_id: RecordTypeID, name: str, type: str):
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        edit.update_field(record_type, name, type)
        self._write_model(model_id)

    @write
    async def record_type_delete_field(self, model_id: ModelID, type_id: RecordTypeID, name: str):
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        edit.remove_field(record_type, name)
        self._write_model(model_id)

    @read
    async def record_type_source(self, model_id: ModelID, type_id: RecordTypeID) -> str:
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        return edit.get_node_source(record_type)

    @write
    async def write_record_type_source(self, model_id: ModelID, type_id: RecordTypeID, update: str) -> None:
        record_type = self.model_set.get_record_type_by_id(type_id, model_id)
        
        new_node_id = edit.update_node_source(record_type,update)
        self._write_model(model_id)
        return new_node_id

    ## Listing reference options (actors, tasks, information spaces, types) ##
    
    @read
    async def actor_affiliation_options(self, model_id, actor_id):
        #An actor can't be affiliated with itself or its own affiliations
        model = self.model_set.get_model_by_id(model_id)
        exclude = set([actor_id])

        exclude.update(list_affiliated_actors(self.model_set, model_id, actor_id))
        exclude.update(list_actor_affiliations(self.model_set, model_id, actor_id))
        
        options = [a.name for a in model.actors if not a.name in exclude]
        return options

    @read
    async def actor_affiliated_options(self, model_id, actor_id):
        #An actor can't add his own affiliations as affiliated actor
        model = self.model_set.get_model_by_id(model_id)
        exclude = set([actor_id])
        exclude.update(list_actor_affiliations(self.model_set, model_id, actor_id))
        return [a.name for a in model.actors if not a.name in exclude]
    
    ## Internal analysis ##
    @read
    async def read_info_space_producers(self, model_id, ifs_id):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return []
    
    @read
    async def read_info_space_consumers(self, model_id, ifs_id):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return []
    
    @read
    async def read_info_space_triggered(self, model_id, ifs_id):
        ifs = self.model_set.get_info_space_by_id(ifs_id, model_id)
        return []
       
    @staticmethod
    def affects(action:str, action_args: list[Any], view: str, view_args: list[Any]) -> bool:
        #Notify on structural changes
        if view == 'plan':
            if action.startswith('create') or action.startswith('delete') or action.startswith('rename') or action.startswith('move'):
                return action_args[0] == view_args[0]
        
            if action in ['actor_add_affiliation','actor_remove_affiliation','actor_add_affiliated','actor_remove_affiliated','task_add_instance','task_remove_instance']:
                return True

        if (view == 'task_info_spaces' or view == 'task_parts') and (action.startswith('create') or action.startswith('delete')):
            return True #TODO: Should be even more specific
        if view == 'list_scenarios' and action in ['create_scenario','delete_scenario']:
            return action_args[0] == view_args[0]
        if view in ['task_parts','plan_tasks'] and action in ['move_task_up','move_task_down','create_task','delete_task']:
            return action_args[0] == view_args[0]
        if action.startswith('plan_') and view.startswith('plan_'):
            return action_args[0] == view_args[0]
        if action.startswith('actor_') and view.startswith('actor_'):
            return action_args[0:2] == view_args[0:2]
        if action.startswith('task_') and view.startswith('task_'):
            return action_args[0:2] == view_args[0:2]
        if action.startswith('info_space_') and view.startswith('info_space_'):
            return action_args[0:2] == view_args[0:2]
        if action.startswith('type_') and view.startswith('type_'):
            return action_args[0:2] == view_args[0:2]
        
        return False
