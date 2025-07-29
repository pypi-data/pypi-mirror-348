"""Structural definition of actor-task-information network models, i.e. the C2Sketch meta-model"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from c2sketch.models.identifier import *

__all__ = [
    'Node','Problem',
    'Model','Import',
    'Attribute','Constraint',
    'Actor','ActorGroup','ActorMember','ActorLocation',
    'Location','LocationGroup','LocationMember',
    'TaskNode','Task','TaskDefinition','TaskInstance','TaskReference',
    'ImplicitTask','ImplicitTaskDefinition','ImplicitTaskInstance',
    'Trigger','InformationSpaceRequirement','InformationSpaceBinding',
    'InformationSpace','FieldMode','AgeLimit','KeyLimit','Record',
    'RecordType','RecordTypeField',
]

class Node:
    """Models are heterogenous recursive tree structures consisting of nodes"""

    #Doubly linked structure for easy traversal
    parent: Node | None
    nodes: list[Node]

    #Markers in source
    source_start: int #Reference to start line in source code
    source_end: int #Reference to end line in source code

    ##All nodes can be decorated with problems identified by static analysis
    problems: list[Problem]

    def __init__(self, parent: Node | None = None, source_start: int = 0, source_end: int = 0):
        self.parent = parent
        self.nodes = []
        self.source_start = source_start
        self.source_end = source_end
        self.problems = []

    @property
    def node_id(self) -> str: #Always return globally qualified identifiers
        return '-'
    
    @property
    def complete_nodes(self) -> list[Node]:
        """List both explicit and implicit nodes"""
        return [node for node in self.nodes]
    
    @property
    def model(self) -> Model:
        if isinstance(self, Model):
            return self
        elif self.parent is None:
            return None
        else:
            return self.parent.model

    @property
    def depth(self) -> int:
        if self.parent is None:
            return 0
        else:
            return self.parent.depth + 1
    
    def get_attribute(self, key: str) -> str | None:
        for node in self.nodes:
            if isinstance(node,Attribute) and node.name == key:
                return node.value
        return None
    
    def get_constraint(self, key: str) -> str | None:
        for node in self.nodes:
            if isinstance(node,Constraint) and node.name == key:
                return node.value
        return None       

class Problem:
    """Result of static model analysis"""
    description: str

    def __init__(self, description: str):
        self.description = description

class Model(Node):
    """Models are the root nodes in which other nodes are defined"""

    #Globally unique identifier of the model
    id: ModelID
    
    #Heterogenous list of model nodes
    nodes: list[Node] = field(default_factory=list)

    #Raw source code 
    source: list[str] = field(default_factory=list)

    def __init__(self, id: ModelID):
        self.id = id
        self.source = []

        super().__init__(parent=None)

    @property
    def title(self) -> str | None:
        return self.get_attribute('title')

    @property
    def summary(self) -> str | None:
        return self.get_attribute('summary')

    @property
    def label(self) -> str:
        return self.id if self.title is None else self.title

    @property
    def node_id(self) -> str:
        return '-'
   
    ## Child nodes

    @property
    def imports(self) -> list[Import]:
        return [node for node in self.nodes if isinstance(node,Import)]
    
    @property
    def actors(self) -> list[Actor]:
        return [node for node in self.nodes if isinstance(node,Actor)]

    @property
    def locations(self) -> list[Location]:
        return [node for node in self.nodes if isinstance(node,Location)]
    
    @property
    def tasks(self) -> list[Task]:
        return [node for node in self.nodes if isinstance(node,Task)]
    
    @property
    def task_definitions(self) -> list[TaskDefinition]:
        return [node for node in self.nodes if isinstance(node,TaskDefinition)]
    
    @property
    def task_instances(self) -> list[TaskInstance]:
        return [node for node in self.nodes if isinstance(node,TaskInstance)]

    @property
    def info_spaces(self) -> list[InformationSpace]:
        return [node for node in self.nodes if isinstance(node,InformationSpace)]
    
    @property
    def record_types(self) -> list[RecordType]:
        return [node for node in self.nodes if isinstance(node,RecordType)]
    
    def get_info_spaces_for_display(self, display_name: str) -> list[InformationSpace]:
        return [ifs for ifs in self.info_spaces if ifs.display == display_name]


class Import(Node):

    reference: ModelID

    def __init__(self, reference: ModelID, parent = None, source_start = 0, source_end = 0):
        self.reference = reference
        super().__init__(parent, source_start, source_end)

class Attribute(Node):
  
    name: str
    value: str

    def __init__(self, name: str, value: str, parent = None, source_start = 0, source_end = 0):
        self.name = name
        self.value = value
        super().__init__(parent, source_start, source_end)


class Constraint(Node):

    name: str
    value: str

    def __init__(self, name: str, value: str, parent = None, source_start = 0, source_end = 0):
        self.name = name
        self.value = value
        super().__init__(parent, source_start, source_end)


class Actor(Node):
  
    name: ActorID

    def __init__(self, name: ActorName, parent = None, source_start = 0, source_end = 0):
        self.name = name
        super().__init__(parent, source_start, source_end)

    @property
    def node_id(self):
        if self.parent is None:
            return self.name
        
        assert isinstance(self.parent,Model)
        return f'{self.name}@{self.parent.id}'
    
    @property
    def title(self) -> str | None:
        return self.get_attribute('title')
  
    @property
    def description(self) -> str | None:
        return self.get_attribute('description')
    
    @property
    def type(self) -> str | None:
        return self.get_attribute('type')
   
    @property
    def color(self) -> str | None:
        return self.get_attribute('color')

    @property
    def label(self) -> str:
        return self.name if self.title is None else self.title

    @property
    def groups(self) -> list[ActorID]:
        model_id = self.model.id
        return [global_id_from_id(node.group_id,model_id) for node in self.nodes if isinstance(node,ActorGroup)]
    
    @property
    def members(self) -> list[ActorID]:
        model_id = self.model.id
        return [global_id_from_id(node.actor_id,model_id) for node in self.nodes if isinstance(node,ActorMember)]
    
    @property
    def locations(self) -> list[LocationID]:
        model_id = self.model.id
        return [global_id_from_id(node.location_id,model_id) for node in self.nodes if isinstance(node,ActorLocation)]
 
class ActorMember(Node):
   
    actor_id: ActorID
 
    def __init__(self, actor_id: ActorID, parent = None, source_start = 0, source_end = 0):
        self.actor_id = actor_id
        super().__init__(parent, source_start, source_end)


class ActorGroup(Node):
 
    group_id: ActorID

    def __init__(self, group_id: ActorID, parent = None, source_start = 0, source_end = 0):
        self.group_id = group_id
        super().__init__(parent, source_start, source_end)


class ActorLocation(Node):
   
    location_id: LocationID
    
    def __init__(self, location_id: LocationID, parent = None, source_start = 0, source_end = 0):
        self.location_id = location_id
        super().__init__(parent, source_start, source_end)


class Location(Node):
   
    name: LocationName

    def __init__(self, name: LocationName, parent = None, source_start = 0, source_end = 0):
        self.name = name
        super().__init__(parent, source_start, source_end)

    @property
    def node_id(self):
        assert self.parent is not None
        return f'{self.name}@{self.parent.node_id}'
    
    @property
    def title(self) -> str | None:
        return self.get_attribute('title')
    
    @property
    def description(self) -> str | None:
        return self.get_attribute('description')

    @property
    def label(self) -> str:
        return self.name if self.title is None else self.title

    @property
    def groups(self) -> list[LocationID]:
        return [node.group_id for node in self.nodes if isinstance(node,LocationGroup)]
    
    @property
    def members(self) -> list[ActorID]:
        return [node.location_id for node in self.nodes if isinstance(node,LocationMember)]
    

class LocationMember(Node):

    location_id: LocationID
    
    def __init__(self, location_id: LocationID, parent = None, source_start = 0, source_end = 0):
        self.location_id = location_id
        super().__init__(parent, source_start, source_end)

class LocationGroup(Node):
   
    group_id: LocationID

    def __init__(self, group_id: LocationID, parent = None, source_start = 0, source_end = 0):
        self.group_id = group_id
        super().__init__(parent, source_start, source_end)

class TaskNode(Node):
    name: str
  
    def __init__(self, name: str, parent = None, source_start = 0, source_end = 0):
        self.name = name
        super().__init__(parent, source_start, source_end)

    @property
    def label(self) -> str:
        return self.name

    @property
    def number(self) -> str:
        return '1'
 
    def is_concrete(self) -> bool:
        """A task is concrete if none of its ancestors is a task definition"""
        node = self
            
        while node is not None and not isinstance(node,Model):
            if isinstance(node,TaskDefinition) or isinstance(node,ImplicitTaskDefinition):
                return False
            node = node.parent
        return True
    
    @property
    def for_actor(self) -> ActorID | None:
        return None
    
    def parameter_scope(self) -> dict[str,Any]:
        if isinstance(self,ImplicitTask) :
            return self.parent.parameter_scope()
        
        if isinstance(self,TaskInstance):
            scope = {} if (isinstance(self.parent,Model) or self.parent is None) else self.parent.parameter_scope()
            if self.parameter:
                scope.update(self.parameter)
            return scope
        if isinstance(self,ImplicitTaskInstance):
            scope = self.parent.parameter_scope()
            if self.template.parameter:
                scope.update(self.template.parameter)
            return scope
        return {}
    
    def expanded_label(self, label: str) -> str:
        parameters = self.parameter_scope()
        for key, value in parameters.items():
            label = label.replace('{'+key+'}',str(value))
        return label

class Task(TaskNode):
   
    def __init__(self, name: TaskName, parent = None, source_start = 0, source_end = 0):
        self.name = name
        super().__init__(name, parent, source_start, source_end)

    @property
    def node_id(self):
        if self.parent is None:
            return self.name
        if isinstance(self.parent,Model): #Root level
            return f'{self.name}@{self.parent.id}'
        else:
            parent_id, model_id = local_id_from_global_id(self.parent.node_id)
            return f'{parent_id}.{self.name}@{model_id}'

    @property
    def title(self) -> str | None:
        return self.get_attribute('title')
   
    @property
    def description(self) -> str | None:
        return self.get_attribute('description')
      
    @property
    def for_actor(self) -> ActorID | None:
        for_actor = self.get_constraint('for-actor')
        return None if for_actor is None else global_id_from_id(for_actor,self.model.id)
     
    @property
    def label(self) -> str:
        return self.name if self.title is None else self.title
    
    ## Child nodes
    @property
    def info_space_requirements(self) -> list[InformationSpaceRequirement]:
        return [node for node in self.nodes if isinstance(node,InformationSpaceRequirement)]
    
    @property
    def triggers(self) -> list[str]:
        return [node.reference for node in self.nodes if isinstance(node,Trigger)]
    
    @property
    def tasks(self) -> list[Task]:
        return [node for node in self.nodes if isinstance(node,Task)]
    
    @property
    def task_definitions(self) -> list[TaskDefinition]:
        return [node for node in self.nodes if isinstance(node,TaskDefinition)]
    
    @property
    def task_instances(self) -> list[TaskInstance]:
        return [node for node in self.nodes if isinstance(node,TaskInstance)]
    
    def is_compound(self) -> bool:
        return len(self.tasks) > 0
    
class TaskDefinition(TaskNode):
    """A parameterized specification of a task that can be instantiated multiple times"""

    parameter_type: RecordTypeID | None = None
    
    def __init__(self, name, parameter_type: RecordTypeID | None = None, parent=None, source_start=0, source_end=0):
        self.parameter_type = parameter_type
        super().__init__(name, parent, source_start, source_end)

    @property
    def node_id(self): #Same as task
        if self.parent is None:
            return self.name
        if isinstance(self.parent,Model): #Root level
            return f'{self.name}@{self.parent.id}'
        else:
            parent_id, model_id = local_id_from_global_id(self.parent.node_id)
            return f'{parent_id}.{self.name}@{model_id}'

    @property
    def title(self) -> str | None:
        return self.get_attribute('title')
    
    @property
    def description(self) -> str | None:
        return self.get_attribute('description')
    
    @property
    def for_actor(self) -> ActorID | None:
        for_actor = self.get_constraint('for-actor')
        return None if for_actor is None else global_id_from_id(for_actor,self.model.id)
    
    @property
    def label(self) -> str:
        return self.name if self.title is None else self.title
        
    ## Child nodes

    @property
    def info_space_requirements(self) -> list[InformationSpaceRequirement]:
        return [node for node in self.nodes if isinstance(node,InformationSpaceRequirement)]
    
    @property
    def triggers(self) -> list[Trigger]:
        return [node for node in self.nodes if isinstance(node,Trigger)]
    
    @property
    def tasks(self) -> list[Task]:
        return [node for node in self.nodes if isinstance(node,Task)]
    
    @property
    def task_definitions(self) -> list[TaskDefinition]:
        return [node for node in self.nodes if isinstance(node,TaskDefinition)]
    
    @property
    def task_instances(self) -> list[TaskInstance]:
        return [node for node in self.nodes if isinstance(node,TaskInstance)]

    def get_instances(self) -> list[TaskInstance]:
        if self.parent is None:
            return []
        return [node for node in self.parent.nodes if isinstance(node,TaskInstance) and node.name == self.name]
    
    def is_compound(self) -> bool:
        return len(self.tasks) > 0

    def is_concrete(self) -> bool:
        return False
   
class TaskInstance(TaskNode):
 
    # Sequence number to identify instances 
    sequence: int

    # The a-priori information that defines the task instance
    parameter: dict[str,Any] | None = None
   
    def __init__(self, name, sequence: int, parameter:dict[str,Any] | None = None, parent=None, source_start=0, source_end=0):
        self.sequence = sequence
        self.parameter = parameter
        super().__init__(name, parent, source_start, source_end)

    @property
    def node_id(self):
        if self.parent is None:
            return f'{self.name}-{self.sequence}' 
        if isinstance(self.parent,Model): #Root level
            return f'{self.name}-{self.sequence}@{self.parent.id}'
        else:
            parent_id, model_id = local_id_from_global_id(self.parent.node_id)
            return f'{parent_id}.{self.name}-{self.sequence}@{model_id}'
    
    @property
    def complete_nodes(self) -> list[Node]:
        """List both explicit and implicit nodes"""

        definition = self.get_definition()
        nodes = []
        #The tasks and instances defined in the definition are implicit 
        for node in definition.nodes:
            if isinstance(node,Task):
                nodes.append(ImplicitTask(node,parent=self))
            elif isinstance(node,TaskDefinition):
                nodes.append(ImplicitTaskDefinition(node,parent=self))
            elif isinstance(node,TaskInstance):
                nodes.append(ImplicitTaskInstance(node,parent=self))
        #Add the explicitly defined nodes 
        nodes.extend(self.nodes)  
        return nodes

    @property
    def for_actor(self) -> ActorID | None:
        for_actor = self.get_constraint('for-actor')
        return None if for_actor is None else global_id_from_id(for_actor,self.model.id)
    
    @property
    def label(self) -> str:
        return self.expanded_label(self.get_definition().label)

    @property
    def info_space_requirements(self) -> list[InformationSpaceRequirement]:
        return self.get_definition().info_space_requirements
    @property
    def info_space_bindings(self)-> list[InformationSpaceBinding]:
        return [node for node in self.nodes if isinstance(node,InformationSpaceBinding)]

    @property
    def task_instances(self) -> list[TaskInstance]:
        return [node for node in self.nodes if isinstance(node,TaskInstance)]

    def get_definition(self) -> TaskDefinition:
        if self.parent is not None:
            for node in self.parent.complete_nodes:
                if isinstance(node,TaskDefinition) and node.name == self.name:
                    return node
            
        raise KeyError(f'Definition of instance {self.name} not found')  
    

class ImplicitTask(TaskNode):

    template: Task

    def __init__(self, template: Task, parent=None, source_start=0, source_end=0):
        self.template = template
        super().__init__(template.name, parent, source_start, source_end)

    @property
    def node_id(self):
        parent_id, model_id = local_id_from_global_id(self.parent.node_id)
        return f'{parent_id}.{self.template.name}@{model_id}'

    @property
    def complete_nodes(self) -> list[Node]:
        nodes = []
        for node in self.template.nodes:
            if isinstance(node,Task):
                nodes.append(ImplicitTask(node,parent=self))
            elif isinstance(node,TaskDefinition):
                nodes.append(ImplicitTaskDefinition(node,parent=self))
            elif isinstance(node,TaskInstance):
                nodes.append(ImplicitTaskInstance(node,parent=self))
        return nodes

    @property
    def for_actor(self) -> ActorID | None:
        return self.template.for_actor
    @property
    def label(self) -> str:
        return self.expanded_label(self.template.label)
     

class ImplicitTaskDefinition(TaskNode):

    template: TaskDefinition

    def __init__(self, template: TaskDefinition, parent=None, source_start=0, source_end=0):
        self.template = template
        super().__init__(template.name, parent, source_start, source_end)

    @property
    def node_id(self):
        parent_id, model_id = local_id_from_global_id(self.parent.node_id)
        return f'{parent_id}.{self.template.name}@{model_id}'
            
    @property
    def complete_nodes(self) -> list[Node]:
        nodes = []
        for node in self.template.nodes:
            if isinstance(node,Task):
                nodes.append(ImplicitTask(node,parent=self))
            elif isinstance(node,TaskDefinition):
                nodes.append(ImplicitTaskDefinition(node,parent=self))
            elif isinstance(node,TaskInstance):
                nodes.append(ImplicitTaskInstance(node,parent=self))
        return nodes
    
    @property
    def for_actor(self) -> ActorID | None:
        return self.template.for_actor
    @property
    def label(self) -> str:
        return self.template.label
    
    @property
    def parameter_type(self) -> RecordTypeID | None:
        return self.template.parameter_type

    def get_instances(self) -> list[TaskInstance|ImplicitTaskInstance]:
        return [node for node in self.parent.complete_nodes 
                if (isinstance(node,TaskInstance) or isinstance(node,ImplicitTaskInstance)) and node.name == self.name]
    

class ImplicitTaskInstance(TaskNode):
  
    template: TaskInstance

    def __init__(self, template: TaskInstance, parent=None, source_start=0, source_end=0):
        self.template = template
        super().__init__(template.name, parent, source_start, source_end)


    @property
    def node_id(self):
        parent_id, model_id = local_id_from_global_id(self.parent.node_id)
        return f'{parent_id}.{self.name}-{self.template.sequence}@{model_id}'

    @property
    def sequence(self) -> int:
        return self.template.sequence
    
    @property
    def parameter(self) -> dict[str,Any] | None:
        return self.template.parameter
    
    @property
    def for_actor(self) -> ActorID | None:
        return self.template.for_actor
    
    @property
    def complete_nodes(self) -> list[Node]:
        definition = self.template.get_definition()
        nodes = []
        for node in definition.nodes:
            if isinstance(node,Task):
                nodes.append(ImplicitTask(node,parent=self))
            elif isinstance(node,TaskDefinition):
                nodes.append(ImplicitTaskDefinition(node,parent=self))
            elif isinstance(node,TaskInstance):
                nodes.append(ImplicitTaskInstance(node,parent=self))
    
        return nodes
    
    @property
    def label(self) -> str:
        return self.expanded_label(self.template.get_definition().label)

    def get_definition(self) -> ImplicitTaskDefinition:
        for node in self.parent.complete_nodes:
            if isinstance(node,ImplicitTaskDefinition) and node.name == self.name:
                return node
        
        raise KeyError(f'Definition of instance {self.name} not found')


class TaskReference(Node):
   
    reference: TaskID

    # The a-priori information that defines the task instance when
    # a task definition is referenced. None if a task is referenced.
    parameter: dict[str,Any] | None = None

    def __init__(self, reference: TaskID, parameter: dict[str,Any] | None = None, parent = None, source_start = 0, source_end = 0):
        self.reference = reference
        self.parameter = parameter
        super().__init__(parent, source_start, source_end)

class Trigger(Node):
  
    def __init__(self, reference: InformationSpaceID, parent = None, source_start = 0, source_end = 0):
        self.reference = reference
        super().__init__(parent, source_start, source_end)

class InformationSpaceRequirement(Node):
    """Allows referencing dynamically bound external information spaces"""
   
    name: str
    type: RecordTypeID | None = None
    read: bool = True
    write: bool = True
    binding: str | None = None #default binding
    
    def __init__(self, name: str, type: RecordTypeID | None = None, read: bool = True, write: bool = True, binding: str | None = None, parent = None, source_start = 1, source_end = 1):
        self.name = name
        self.type = type
        self.read = read
        self.write = write
        self.binding = binding
        super().__init__(parent, source_start, source_end)


class InformationSpaceBinding(Node):
  
    name: str #References an information space requirement with the same name
    binding: str #References an information space from the task scope

    def __init__(self, name: str, binding: str, parent = None, source_start = 0, source_end = 0):
        self.name = name
        self.binding = binding
        super().__init__(parent, source_start, source_end)

class InformationSpace(Node):
   
    name: InformationSpaceName
    type: RecordTypeID | None = None

    def __init__(self,name: InformationSpaceName, type: RecordTypeID | None = None, parent = None, source_start = 0, source_end = 0):
        self.name = name
        self.type = type
        
        super().__init__(parent, source_start, source_end)

    @property
    def node_id(self):
        if self.parent is None:
            return self.name
        if isinstance(self.parent,Model): #Root level
            return f'{self.name}@{self.parent.id}'
        else:
            parent_id, model_id = local_id_from_global_id(self.parent.node_id)
            return f'{parent_id}.{self.name}@{model_id}'
        
    @property
    def title(self) -> str | None:
        return self.get_attribute('title')
   
    @property
    def description(self) -> str | None:
        return self.get_attribute('description') 
   
    @property
    def color(self) -> str | None:
        return self.get_attribute('color')
   
    @property
    def label(self) -> str:
        return self.name if self.title is None else self.title 

    @property
    def display(self) -> str | None:
        return self.get_attribute('display')
    
    @property
    def graphic_type(self) -> str | None:
        return self.get_attribute('graphic-type')
    
    @property
    def records(self) -> list[Record]:
        return [node for node in self.nodes if isinstance(node,Record)]

    @property
    def at_location(self) -> LocationID | None:
        at_location = self.get_constraint('at-location')
        return None if at_location is None else global_id_from_id(at_location,self.model.id)
    
    @property
    def for_actor(self) -> ActorID | None:
        for_actor = self.get_constraint('for-actor')
        return None if for_actor is None else global_id_from_id(for_actor,self.model.id)

    @property
    def key_field(self) -> str | None:
        for node in self.nodes:
            if isinstance(node,FieldMode) and node.mode == 'key':
                return node.field_name
        return None

    @property
    def field_modes(self) -> dict[str,str]:
        modes = {}
        for node in self.nodes:
            if isinstance(node,FieldMode):
                modes[node.field_name] = node.mode
        return modes
    
    @property
    def age_limit(self) -> int | None:
        for node in self.nodes:
            if isinstance(node,AgeLimit):
                return node.limit
        return None

    @property
    def key_limit(self) -> int | None:
        for node in self.nodes:
            if isinstance(node,KeyLimit):
                return node.limit
        return None

    def last_updated(self) -> int | None:
        return self.records[-1].create_time if self.records else None
    

class FieldMode(Node):

    field_name: str
    mode: str # key | first | last | min | max

    def __init__(self, field_name: str, mode: str, parent = None, source_start = 0, source_end = 0):
        self.field_name = field_name
        self.mode = mode
        super().__init__(parent, source_start, source_end)


class AgeLimit(Node):
   
    limit: int

    def __init__(self, limit: int, parent = None, source_start = 0, source_end = 0):
        self.limit = limit
        super().__init__(parent, source_start, source_end)

@dataclass(eq=False)
class KeyLimit(Node):

    limit: int

    def __init__(self, limit: int, parent = None, source_start = 0, source_end = 0):
        self.limit = limit
        super().__init__(parent, source_start, source_end)


class Record(Node):

    fields: dict[str,Any]

    #Meta-data
    sequence_number: int = 0

    create_time: int = 0
    create_actor: ActorID | None = None
    create_location: LocationID | None = None

    def __init__(self, fields: dict[str,Any], sequence_number: int = 0,
                 create_time: int = 0, create_actor: ActorID | None = None, create_location: LocationID | None = None,
                 parent = None, source_start = 1, source_end = 1):
        self.fields = fields
        self.sequence_number = sequence_number
        self.create_time = create_time
        self.create_actor = create_actor
        self.create_location = create_location

        super().__init__(parent, source_start, source_end)

    def inline_references(self, values: Record) -> Record:
        inlined = {}
        for key,value in self.fields.items():
            if isinstance(value,str) and values is not None:
                try:
                    inlined[key] = value.format(**values.fields)
                except KeyError: #If a specified replacement is not available, just use the value
                    inlined[key] = value
            else:
                inlined[key] = value
        return Record(inlined, parent = values.parent)

class RecordType(Node):
  
    name: RecordTypeName
    
    def __init__(self, name: RecordTypeName, parent = None, source_start = 0, source_end = 0):
        self.name = name
        super().__init__(parent, source_start, source_end)

    def __str__(self):
        fields = ','.join(f'{field.name}: {field.type}' for field in self.fields)
        return f'{fields}'
    
    @property
    def node_id(self):
        if self.parent is None:
            return self.name
        return f'{self.name}@{self.parent.id}'
        
    @property
    def fields(self) -> list[RecordTypeField]:
        return [node for node in self.nodes if isinstance(node,RecordTypeField)]

class RecordTypeField(Node):
  
    name: str
    type: RecordTypeID | PrimitiveTypeID | None

    def __init__(self, name: str, type: RecordTypeID | PrimitiveTypeID | None = None, parent = None, source_start = 0, source_end = 0):
        self.name = name
        self.type = type
        super().__init__(parent, source_start, source_end)