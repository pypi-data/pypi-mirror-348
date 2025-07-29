"""
This module provides types and utility functions for the various structured
identifiers of parts of network models and executions.
"""

__all__ = [
    'SafeName',
    'ModelID',
    'NodeID',
    'ActorName','ActorID',
    'LocationName','LocationID',
    'TaskName','TaskID','TaskInstanceID',
    'InformationSpaceName','InformationSpaceID',
    'PrimitiveTypeName','PrimitiveTypeID','RecordTypeName','RecordTypeID',
    'ScenarioName','ScenarioID',
    'parent_from_id','child_id','is_local_id','is_global_id','local_id_from_global_id','global_id_from_id',
    'name_from_task_id','name_from_actor_id','name_from_model_id',
    'is_top_level','task_id_from_instance_id','task_from_id',
    'is_safe_name','to_safe_name'
]


# To uniquely identify individual items in models (and collections of models) we use strings
# that are safe to use in many programming languages, this makes generating code
# or data formats easier.
# All model elements also have title attributes without any restrictions

SafeName = str

def is_safe_name(name: str) -> bool:
    """Safe names:
       - are not empty
       - start with an underscore or letter
       - contain only underscores and alphanumeric characters
    """
    if len(name) == 0:
        return False
    if (not name[0].isalpha()) and (not name[0] == '_'):
        return False
    return all(c.isalnum() or (c == '_') for c in name[1:])

def is_dotted_safe_name(name: str) -> bool:
    return all(map(is_safe_name,name.split('.')))

def to_safe_name(name: str) -> str:
    safe = list()
    for c in name:
        if c.isspace():
            safe.append('_')
        if c.isdigit() or c.isalpha():
            safe.append(c)
    if len(safe) == 0:
        return 'untitled'

    if safe[0].isdigit():
        safe.insert(0,'_')
    return  ''.join(safe)

# Identifiers for models:
# We use a global hierarchic naming scheme that uses dotted safe names
# E.g. mycollection.mymodel or c2sketch.prelude

ModelID = str

def is_model_id(id: str) -> bool:
    return is_dotted_safe_name(id)


# Identifiers for actors"
# Actors are uniquely named local to a model.
# Therefore locally ActorID's are simply safe names.
# E.g. My_Actor or my_organization
# To enable referencing actors from other models, ActorID's may contain
# a suffix of an @ followed by a mision model id.
# E.g. Other_Actor@collection.other_module

ActorName = SafeName
ActorID = str

def is_actor_id(id: str) -> bool:
    at_pos = id.find('@')
    if at_pos == -1:
        return is_safe_name(id)
    else:
        return is_safe_name(id[:at_pos]) and is_model_id(id[at_pos+1:]) 

# Identifiers for locations
LocationName = SafeName
LocationID = str

# Identifiers for tasks, task instances and task definitions:
# Tasks are uniquely named local to the mission model, or to another task.
# TaskID's are therefore identified as dotted safe names local to a model.
# E.g. main_task.sub_task_a.do_something or another_main_task
# To enable referencing tasks from other model, TaskID's may also contain
# a suffix of an @ followed by a mision model id.
# E.g. main_task@collection.other_module



TaskName = SafeName
TaskID = str

def is_task_id(id: str) -> bool:
    at_pos = id.find('@')
    if at_pos == -1:
        return is_dotted_safe_name(id)
    else:
        return is_dotted_safe_name(id[:at_pos]) and is_model_id(id[at_pos+1:]) 

# To reference concrete instances of task definitions (which are also tasks), each concrete task instance is
# given a sequence number.
# The names ofthe (sub)tasks combined with the (sub)task numbers identify instances.
# Sequence numbers are added to task names using a '-'.
# Non-parametric tasks implicitly have sequence number 1. The '-1' suffix may be omitted.
# E.g taskname-23.subtaskname-12
# TaskInstanceID's can also reference other modules using the @ notation
# E.g. main_task-1@some.other_module

TaskInstanceID = str

def is_task_instance_id(id: str) -> bool:

    def is_local_task_instance_instance_id(local_id: str) -> bool:
        for part in local_id.split('.'):
            match part.split('-'):
                case [task_name]:
                    if not is_safe_name(task_name):
                        return False
                case [task_name,sequence_number]:
                    if not is_safe_name(task_name) or not sequence_number.isdigit():
                        return False
                case _:
                    return False
        return True

    at_pos = id.find('@')
    if at_pos == -1:
        return is_local_task_instance_instance_id(id)
    else:
        return is_local_task_instance_instance_id(id[:at_pos]) and is_model_id(id[at_pos+1:]) 

# Identifiers for information spaces:
# Information spaces are identified by a unique name local to a mission model
# or to a task.
# There identifiers are therefore similar to tasks identifiers, dotted safe names,
# but the last part of the dotted id is interpreted as an OP name instead of a task name.
# E.g. main_task.subtask.picture1 or simply picture2
# InformationSpaceID's can also reference other model using the @ notation
# E.g. main_ifs@some.other_module

InformationSpaceName = SafeName
InformationSpaceID = str

def is_information_space_id(id: str) -> bool:
    at_pos = id.find('@')
    if at_pos == -1:
        return is_dotted_safe_name(id)
    else:
        return is_dotted_safe_name(id[:at_pos]) and is_model_id(id[at_pos+1:])

# Identifiers for data types:
# Types have similiar identifiers as actors.
# They are uniquely named local to a mission model.
# They can also be referenced other models using the @notation

# Primitive types are the built-in datatypes to contruct more complex structures with
# Predefined values:
# - 'string'    : Short (single line) text value
# - 'text'      : Long (multi line) text values
# - 'integer'   : Scalar integer
# - 'float'     : Scalar floating point value
# - 'boolean'   : True/False
# - 'byte'      : Single byte
# - 'timestamp' : Timestamp with seconds precision
# - 'latlng'    : Geographic interpretation of 2d real vector

PrimitiveTypeName = SafeName
PrimitiveTypeID = str

RecordTypeName = SafeName
RecordTypeID = str

def is_record_type_id(id: str) -> bool:
    at_pos = id.find('@')
    if at_pos == -1:
        return is_safe_name(id)
    else:
        return is_safe_name(id[:at_pos]) and is_model_id(id[at_pos+1:]) 

# If of a node in a model
NodeID = ActorID | LocationID | TaskID | InformationSpaceID | PrimitiveTypeID | RecordTypeID

# Identifiers for scenarios:
ScenarioName = SafeName
ScenarioID = str

def is_global_id(id: str) -> bool:
    return '@' in id

def is_local_id(id: str) -> bool:
    return '@' not in id

def local_id_from_global_id(id: str) -> tuple[str,ModelID]:
    at_pos = id.find('@')
    if at_pos < 0:
        raise ValueError(f'{id} is not a global identifier')
    return (id[:at_pos],id[at_pos+1:])

def global_id_from_id(id: str, model_id: ModelID) -> str: 
    return id if is_global_id(id) else f'{id}@{model_id}'
   
def name_from_model_id(model_id: ModelID) -> str:
    return model_id[model_id.rfind('.')+1:]
   
def instance_id_from_task_id(task_id: TaskID) -> TaskInstanceID:
    return '.'.join([f'{part}-1' for part in task_id.split('.')])

def parent_from_id(task_id: TaskID) -> TaskID | None:
    if is_local_id(task_id):
        return task_id[:task_id.rfind('.')] if '.' in task_id else None
    else:
        node_id, model_id = local_id_from_global_id(task_id)
        return global_id_from_id(node_id[:node_id.rfind('.')],model_id) if '.' in node_id else None

def child_id(task_id: TaskID, child_name: TaskName) -> TaskID | None:
    if is_local_id(task_id):
        return f'{task_id}.{child_name}'
    else:
        node_id, model_id = local_id_from_global_id(task_id)
        return global_id_from_id(f'{node_id}.{child_name}',model_id)

def name_from_actor_id(actor_id: ActorID):
    return actor_id if is_local_id(actor_id) else local_id_from_global_id(actor_id)[0]

def name_from_task_id(task_id: TaskID) -> str:
    local_id = task_id if is_local_id(task_id) else local_id_from_global_id(task_id)[0]
    #Take last segment of dotted id
    instance_name = local_id[local_id.rfind('.')+1:]
    #Remove dash suffix for instances
    return instance_name[:instance_name.find('-')] if '-' in instance_name else instance_name

def name_from_info_space_id(ifs_id: InformationSpaceID) -> str:
    return ifs_id[ifs_id.rfind('.')+1:]
    
def task_from_id(task_id: TaskID) -> str:
    return task_id[task_id.find('.')+1:]
    
def task_id_from_instance_id(instance_id: TaskInstanceID):
    return '.'.join(p[0] for p in [s.split("-") for s in instance_id.split('.')])

def parent_task_instance_id(instance_id: TaskInstanceID) -> TaskInstanceID | None:
    return instance_id[:instance_id.rfind('.',0,instance_id.rfind('.'))]

def is_instance_id(instance_id: str) -> bool:
    if not isinstance(instance_id,str):
        return False
    for part in instance_id.split('.'):
        sub_parts = part.split('-')
        if len(sub_parts) > 2 or (len(sub_parts) == 2 and not sub_parts[1].isnumeric()):
            return False
    return True

def is_top_level(task_id: TaskID) -> bool:
    
    if is_local_id(task_id):
        return '.' not in task_id
    else:
        return '.' not in local_id_from_global_id(task_id)[0] 
