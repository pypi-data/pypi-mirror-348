from c2sketch.models.structure import Node, Model, Attribute, Constraint, Import, Actor, ActorLocation, ActorGroup, LocationGroup, LocationMember
from c2sketch.models.structure import ActorMember, Location, Task, TaskDefinition, ImplicitTaskDefinition, TaskInstance, ImplicitTaskInstance, InformationSpace, RecordType, RecordTypeField, Problem
from c2sketch.models.structure import TaskNode, InformationSpaceRequirement, InformationSpaceBinding, Trigger, Record
from c2sketch.models.identifier import ModelID, ActorName, LocationName, RecordTypeName, ActorID, LocationID, RecordTypeID
from c2sketch.models.identifier import local_id_from_global_id

from c2sketch.write.model import model_node_to_c2s_str
from c2sketch.read.model import model_from_c2s_str, model_node_from_c2s_str, C2SSyntaxError

from typing import Any

def _indent(lines: list[str], levels: int) -> list[str]:
    return [('    ' * levels) + line for line in lines]
    
def _dedent(lines: list[str], levels: int) -> list[str]:
    return [line[4*levels:] for line in lines]

def _adjust_source_size(node: Node, adjustment: int):

    """Adjusts the nodes end positition, and also adjust the following siblings"""
    #Follow the path back to the root and adjust all siblings
    parent = node.parent
    while parent is not None:
        if node.source_end is not None:
            node.source_end += adjustment

        index = parent.nodes.index(node)
        for i in range(index + 1,len(parent.nodes)):
            _adjust_source_position(parent.nodes[i],adjustment)
        
        node = parent
        parent = node.parent

    if node.source_end is not None:
        node.source_end += adjustment
        
def _adjust_source_position(node: Node, adjustment: int):
    if adjustment == 0:
        return
    
    node.source_start += adjustment
    node.source_end += adjustment

    for sub_node in node.nodes:
        _adjust_source_position(sub_node, adjustment)

def _introduce_colon(node: Node):
    model = node.model
    if model is None or model.source is None:
        return
    if '#' in model.source[node.source_start]: #Retain comments
        comment_start = model.source[node.source_start].find('#')
        model.source[node.source_start] = model.source[node.source_start][:comment_start] + ':' + model.source[node.source_start][comment_start:]
    else:
        model.source[node.source_start] += ':'

def _remove_colon(node: Node):
    model = node.model
    if model is None or model.source is None:
        return
    model.source[node.source_start] = model.source[node.source_start].replace(':','',1) #Remove colon from node definition line

def _correct_instance_sequence_numbers(node: Node):
    numbers = {}
    for child in node.nodes:
        if isinstance(child, TaskInstance):
            if child.name in numbers:
                child.sequence = numbers[child.name] + 1
                numbers[child.name] = numbers[child.name] + 1 
            else:
                child.sequence = 1
                numbers[child.name] = 1

def _correct_record_sequence_numbers(node: Node):
    number = 1
    for child in node.nodes:
        if isinstance(child, Record):
            child.sequence_number = number
            number += 1
                          
def insert_node(parent: Node, index: int, insert_node: Node, insert_source: str):
 
    if isinstance(parent,Model):
        insert_lines = insert_source.splitlines()
        
        if index > 0:
            prev_sibling = parent.nodes[index - 1]
            _adjust_source_position(insert_node,prev_sibling.source_end + 1)
            parent.source = parent.source[:prev_sibling.source_end+1] + insert_lines +  parent.source[prev_sibling.source_end+1:]
        else:
            parent.source = insert_lines + parent.source

        #Adjust siblings
        adjustment = len(insert_lines)
        for i in range(index,len(parent.nodes)):
            _adjust_source_position(parent.nodes[i],adjustment)

        insert_node.parent = parent
        parent.nodes.insert(index,insert_node)
        return
        
    #Insert with adjusted start position
    insert_index = parent.source_start + 1 if index == 0 else parent.nodes[index-1].source_end + 1
    insert_node.parent = parent
    _adjust_source_position(insert_node,insert_index)
    parent.nodes.insert(index,insert_node)
    
    #Update source code
    insert_lines = _indent(insert_source.splitlines(),parent.depth)

    model = parent.model
    if model is not None:
        model.source = model.source[:insert_index] + insert_lines + model.source[insert_index:]

    adjustment = len(insert_lines)
    _adjust_source_size(parent,adjustment)
    for i in range(index + 1,len(parent.nodes)):
        _adjust_source_position(parent.nodes[i],adjustment)

    if len(parent.nodes) == 1: #Add colon
        _introduce_colon(parent)
    
    if isinstance(insert_node, TaskInstance):
        _correct_instance_sequence_numbers(parent)
    if isinstance(insert_node, Record):
        _correct_record_sequence_numbers(parent)


def append_node(parent: Node, insert_node: Node, insert_source: str):
    
    if isinstance(parent,Model):
        insert_lines = insert_source.splitlines()
        _adjust_source_position(insert_node,len(parent.source))
        parent.source = parent.source + insert_lines
        insert_node.parent = parent
        parent.nodes.append(insert_node)
        if isinstance(insert_node, TaskInstance):
            _correct_instance_sequence_numbers(parent)
        if isinstance(insert_node, Record):
            _correct_record_sequence_numbers(parent)
        return
        
    #Append with adjusted start position
    _adjust_source_position(insert_node,parent.source_end + 1)
    insert_node.parent = parent
    parent.nodes.append(insert_node)
    
    #Update source code
    insert_lines = _indent([line for line in insert_source.splitlines()],parent.depth)
    
    model = parent.model
    model.source = model.source[:parent.source_end + 1] + insert_lines + model.source[parent.source_end + 1:]

    _adjust_source_size(parent,len(insert_lines))

    if len(parent.nodes) == 1: #Add colon
        _introduce_colon(parent)

    if isinstance(insert_node, TaskInstance):
        _correct_instance_sequence_numbers(parent)
    if isinstance(insert_node, Record):
        _correct_record_sequence_numbers(parent)

def replace_node(parent: Node, index: int, replacement_node: Node, replacement_source: str) -> Node:
   
    cur_node = parent.nodes[index]
   
    new_node_lines = _indent(replacement_source.splitlines(), parent.depth)
    _adjust_source_position(replacement_node, cur_node.source_start)
    model = cur_node.model
    model.source = model.source[:cur_node.source_start] + new_node_lines + model.source[cur_node.source_end + 1:]
    adjustment = len(new_node_lines) - (cur_node.source_end - cur_node.source_start + 1)
    _adjust_source_size(cur_node, adjustment)

    replacement_node.parent = parent
    parent.nodes[index] = replacement_node

    if isinstance(replacement_node,TaskInstance): #Correct sequence numbers
        _correct_instance_sequence_numbers(parent)
    if isinstance(replacement_node,Record):
        _correct_record_sequence_numbers(parent)
    
    return replacement_node

def remove_node(parent: Node, index: int):

    cur_node = parent.nodes[index]
    was_task_instance = isinstance(cur_node,TaskInstance)
    was_record = isinstance(cur_node,Record)
      
    model = cur_node.model
    model.source = model.source[:cur_node.source_start] + model.source[cur_node.source_end+1:]
    
    adjustment = - (cur_node.source_end - cur_node.source_start + 1)
    _adjust_source_size(cur_node,adjustment)

    parent.nodes.pop(index)
    if not parent.nodes:
        _remove_colon(parent)
    
    if was_task_instance:
        _correct_instance_sequence_numbers(parent)
    if was_record:
        _correct_record_sequence_numbers(parent)

def get_node_source(node: Node) -> str:
    model = node.model
    if model.source:
        return '\n'.join(_dedent(model.source[node.source_start:node.source_end+1],node.depth - 1))
    else:
        return model_node_to_c2s_str(node)

def update_node_source(node: Node, source: str) -> None:
    
    if isinstance(node, Model):
       
        new_model = model_from_c2s_str(node.id, source, True)

        node.source = source.splitlines()
        node.nodes = []
        node.problems = new_model.problems

        for sub_node in new_model.nodes:
            sub_node.parent = node
            node.nodes.append(sub_node)
        return None
    
    if node.parent is None:
        return None

    node_index = node.parent.nodes.index(node)
    try:
        new_node = model_node_from_c2s_str(source, node.__class__)
        replaced_node = replace_node(node.parent,node_index,new_node,source)
        return local_id_from_global_id(replaced_node.node_id)[0]
    except C2SSyntaxError as e:
        #Change the entire model to an unparsable node
        model_node = node.model
        new_node_lines = _indent(source.splitlines(), node.parent.depth)
        model_node.nodes = []
        model_node.source = model_node.source[:node.source_start - 1] + new_node_lines + model_node.source[node.source_end:]
        model_node.problems = [Problem(e.msg)]
        return None

def set_attribute(node: Node, name: str, value:str) -> None:
    value_lines = value.splitlines()
    new_node = Attribute(name, value, node, source_end = 0 if len(value_lines) == 1 else len(value_lines))
    new_node_src = model_node_to_c2s_str(new_node)
    new_pos = 0
    for index, sub_node in enumerate(node.nodes):
        if isinstance(sub_node,Attribute):
            if sub_node.name == name:
                replace_node(node, index, new_node, new_node_src)
                return
            else:
                new_pos = index + 1

    insert_node(node,new_pos,new_node,new_node_src)

def del_attribute(node: Node, name: str) -> None:
    for index, sub_node in enumerate(node.nodes):
        if isinstance(sub_node,Attribute) and sub_node.name == name:
            print("Removing",sub_node.name)
            remove_node(node,index)
            return

def set_constraint(node: Node, name: str, value:str) -> None:
    value_lines = value.splitlines()
    new_node = Constraint(name, value, node, source_end = 0 if len(value_lines) == 1 else len(value_lines))
    new_node_src = model_node_to_c2s_str(new_node)
    new_pos = 0
    for index, sub_node in enumerate(node.nodes):
        if isinstance(sub_node,Constraint):
            if sub_node.name == name:
                replace_node(node, index, new_node, new_node_src)
                return
            else:
                new_pos = index + 1
        elif isinstance(sub_node,Attribute): #Add constraints after attributes
            new_pos = index + 1

    insert_node(node,new_pos,new_node,new_node_src)

def del_constraint(node: Node, name: str) -> None:
    for index, sub_node in enumerate(node.nodes):
        if isinstance(sub_node,Constraint) and sub_node.name == name:
            remove_node(node,index)
            return
        
def move_node_up(node: Node):
    if node.parent is None:
        return
    container = node.parent.nodes
    index = container.index(node)
    if index > 0:
        item = container.pop(index)
        container.insert(index-1,item)
        
def move_down(node: Node):
    if node.parent is None:
        return
    container = node.parent.nodes
    index = container.index(node)
    if index < len(container) - 1:
        item = container.pop(index)
        container.insert(index+1,item)

 ## Model manipulation methods

def add_import(model: Model, reference: ModelID) -> None:
    if reference in (node.reference for node in model.imports):
        raise ValueError(f'Model id "{reference}" already imported')
    
    node = Import(reference)
    append_node(model, node, model_node_to_c2s_str(node))
    
def remove_import(model: Model, reference: ModelID) -> None:
    for index, node in enumerate(model.nodes):
        if isinstance(node,Import) and node.reference == reference:
            return remove_node(model,index)
        
def add_actor(model: Model, name: ActorName, title: str | None, description: str | None = None, type: str | None = None) -> Actor:
    if name in [a.name for a in model.actors]:
        raise ValueError(f'Actor name "{name}" already exists')

    node = Actor(name)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)
    if type is not None and type != '':
        set_attribute(node,'type',type)

    append_node(model,node,model_node_to_c2s_str(node))
        
    return node

def add_actor_group(parent: Actor, group_id: ActorID) -> ActorGroup:
    node = ActorGroup(group_id)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_actor_group(parent: Actor, group_id: ActorID) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,ActorGroup) and node.group_id == group_id:
            remove_node(parent,index)
            return
        
def add_actor_member(parent: Actor, member_id: ActorID) -> ActorMember:
    node = ActorMember(member_id)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_actor_member(parent: Actor, member_id: ActorID) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,ActorMember) and node.actor_id == member_id:
            remove_node(parent,index)
            return
              
def add_actor_location(parent: Actor, location_id: LocationID) -> ActorLocation:
    node = ActorLocation(location_id)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_actor_location(parent: Actor, location_id: LocationID) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,ActorLocation) and node.location_id == location_id:
            remove_node(parent,index)
            return

def remove_actor(node: Actor):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_location(model: Model, name: LocationName, title: str | None, description: str | None = None) -> Location:
    if name in [l.name for l in model.locations]:
        raise ValueError(f'Location name "{name}" already exists')
    node = Location(name)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)

    append_node(model,node,model_node_to_c2s_str(node))
    return node

def add_location_group(parent: Location, group_id: LocationID) -> LocationGroup:
    node = LocationGroup(group_id)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_location_group(parent: Location, group_id: LocationID) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,LocationGroup) and node.group_id == group_id:
            remove_node(parent,index)
            return
        
def add_location_member(parent: Location, member_id: LocationID) -> LocationMember:
    node = LocationMember(member_id)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_location_member(parent: Location, member_id: LocationID) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,LocationMember) and node.location_id == member_id:
            remove_node(parent,index)
            return

def remove_location(node: Location):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_task(parent: Model | Task | TaskDefinition, name: str, title: str | None, description: str | None = None) -> Task:
    
    if name in [t.name for t in parent.tasks]:
        raise ValueError(f'Task "{name}" already exists')
    
    node = Task(name)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)
   
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_task(node: Task):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_task_definition(parent: Model | Task, name: str, type: str, title: str | None, description: str | None = None) -> TaskDefinition:
    if name in [t.name for t in parent.task_definitions]:
        raise ValueError(f'Task definition "{name}" already exists')
    
    node = TaskDefinition(name, type)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)
   
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_task_def_type(node: TaskDefinition, type: RecordTypeName | None) -> None:
    if type == node.parameter_type: #Nothing to change
        return 
    node.parameter_type = type
    model = node.model

    header_line = _indent(model_node_to_c2s_str(node).splitlines(),node.parent.depth)[0]
    model.source[node.source_start] = header_line

def remove_task_definition(node: TaskDefinition):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_task_instance(parent: Model | Task, name: str, parameter: dict[str,Any], title: str | None, description: str | None = None) -> TaskInstance:

    node = TaskInstance(name, 1, parameter)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)
   
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_task_instance_parameter(node: TaskInstance, parameter: dict[str,Any] | None) -> None:
    
    if parameter == node.parameter: #Nothing to change
        return 
    node.parameter = parameter
    model = node.model

    header_line = _indent(model_node_to_c2s_str(node).splitlines(),node.parent.depth)[0]
    model.source[node.source_start -1] = header_line

def remove_task_instance(node: TaskInstance):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_info_space(model: Model, name: str, title: str | None = None, description: str | None = None, type: str | None = None) -> InformationSpace:
    if name in (ifs.name for ifs in model.info_spaces):
        raise ValueError(f'Information space "{name}" already exists')
    node = InformationSpace(name,type)
    if title is not None and title != '':
        set_attribute(node,'title',title)
    if description is not None and description != '':
        set_attribute(node,'description',description)
   
    append_node(model,node,model_node_to_c2s_str(node))
    return node

def update_info_space_type(node: InformationSpace, type: RecordTypeID | None) -> None:
    if type == node.type: #Nothing to change
        return 
    node.type = type
    model = node.model

    header_line = _indent(model_node_to_c2s_str(node).splitlines(),node.parent.depth)[0]
    model.source[node.source_start] = header_line

def create_record(parent: InformationSpace, fields: dict[str,str]) -> Record:
    node = Record(fields)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_record(parent: InformationSpace, sequence_number: int, fields: dict[str,str]):
    new_node = Record(fields)
    new_node_src = model_node_to_c2s_str(new_node)

    for index, sub_node in enumerate(parent.nodes):
        if isinstance(sub_node,Record) and sub_node.sequence_number == sequence_number:
            replace_node(parent, index, new_node, new_node_src)
            return

def remove_record(parent: InformationSpace, sequence_number: int) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,Record) and node.sequence_number == sequence_number:
            remove_node(parent,index)
            return

def remove_info_space(node: InformationSpace):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_record_type(model: Model, name: RecordTypeName) -> RecordType:
    if name in (t.name for t in model.record_types):
        raise ValueError(f'Record type "{name}" already exists')
    
    node = RecordType(name)
    append_node(model,node,model_node_to_c2s_str(node))
    return node

def add_field(parent: RecordType, name: str, type: str  ) -> RecordTypeField:
    
    node = RecordTypeField(name, type)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_field(parent: RecordType, name: str, type: str) -> RecordTypeField:
    
    new_node = RecordTypeField(name, type)
    new_node_src = model_node_to_c2s_str(new_node)

    for index, sub_node in enumerate(parent.nodes):
        if isinstance(sub_node,RecordTypeField) and sub_node.name == name:
            replace_node(parent, index, new_node, new_node_src)
            return

def remove_field(parent: RecordType, name: str) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,RecordTypeField) and node.name == name:
            remove_node(parent,index)
            return

def remove_record_type(node: RecordType):
    remove_node(node.parent,node.parent.nodes.index(node))

def add_info_req(parent: TaskNode, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None ) -> InformationSpaceRequirement:
    
    node = InformationSpaceRequirement(name, type, read, write, binding)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_info_req(parent: TaskNode, name: str, type: str | None = None, read: bool = False, write: bool = False, binding: str | None = None ) -> InformationSpaceRequirement:
    
    new_node = InformationSpaceRequirement(name, type, read, write, binding)
    new_node_src = model_node_to_c2s_str(new_node)

    for index, sub_node in enumerate(parent.nodes):
        if isinstance(sub_node,InformationSpaceRequirement) and sub_node.name == name:
            replace_node(parent, index, new_node, new_node_src)
            return

def remove_info_req(parent: Node, name: str) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,InformationSpaceRequirement) and node.name == name:
            remove_node(parent,index)
            return
        
def add_trigger(parent: TaskNode, reference: str) -> Trigger:
    
    node = Trigger(reference)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def remove_trigger(parent: Node, reference: str) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,Trigger) and node.reference == reference:
            remove_node(parent,index)
            return

def add_info_binding(parent: TaskNode, name: str, binding: str | None = None ) -> InformationSpaceBinding:
    
    node = InformationSpaceBinding(name, binding)
    append_node(parent,node,model_node_to_c2s_str(node))
    return node

def update_info_binding(parent: TaskNode, name: str, binding: str | None = None ) -> InformationSpaceBinding:
    
    new_node = InformationSpaceBinding(name, binding)
    new_node_src = model_node_to_c2s_str(new_node)

    for index, sub_node in enumerate(parent.nodes):
        if isinstance(sub_node,InformationSpaceRequirement) and sub_node.name == name:
            replace_node(parent, index, new_node, new_node_src)
            return

def remove_info_binding(parent: Node, name: str) -> None:
    for index, node in enumerate(parent.nodes):
        if isinstance(node,InformationSpaceBinding) and node.name == name:
            remove_node(parent,index)
            return
 
