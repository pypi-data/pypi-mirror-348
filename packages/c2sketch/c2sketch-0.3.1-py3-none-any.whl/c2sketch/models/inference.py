"""Functions for infering information from a model"""
from __future__ import annotations

from .identifier import *
from .structure import *
from .collection import *
from typing import Any

__all__ = [
    'InformationSpaceBindings',
    'resolve_task_actor_constraints',
    'list_valid_bindings',
    'resolve_info_space_bindings',
    'resolve_trigger_bindings',
    'resolve_parameter_value',
    'resolve_indirect_imports',
    'collect_atomic_task_nodes',
    'list_actor_affiliations',
    'list_affiliated_actors',
    'list_individuals',
    'list_concrete_atomic_tasks',
    'list_actor_locations',
    'collect_actor_concrete_atomic_tasks',
    'collect_actor_concrete_task_definitions',
    'collect_actor_information_spaces',
    'recent_records',
    'indexed_fields',
    'actors_at_location',
    'instance_exists'
]

def resolve_task_actor_constraints(node: TaskNode) -> list[ActorID]:
    """Determine the chain of actor constraints for a given task node"""

    constraints = resolve_task_actor_constraints(node.parent) if isinstance(node.parent,TaskNode) else []

    if isinstance(node,TaskInstance) or isinstance(node,ImplicitTaskInstance):
        for_actor = node.get_definition().for_actor
        if for_actor is not None and for_actor not in constraints:
            constraints.append(for_actor)

    for_actor = node.for_actor
    if for_actor is not None and for_actor not in constraints:
        constraints.append(for_actor)
    
    return constraints

def resolve_task_location_constraints(node: Task | TaskDefinition | TaskInstance) -> list[LocationID]:
    """Determine the chain of location constraints given task node"""
    raise NotImplementedError()


def list_valid_bindings(models: ModelSet, node: TaskNode) -> list[InformationSpaceID | str]:
   
    if isinstance(node.parent,Model):
        names = []
        for model_id in resolve_indirect_imports(models,node.parent.id):
            model = models.get_model_by_id(model_id)
            names.extend([ifs.node_id for ifs in model.info_spaces])
        return names
    if isinstance(node.parent, Task) or isinstance(node.parent,TaskDefinition):
        return [req.name for req in node.parent.info_space_requirements]
    return []

#A record with the requirement and its binding for each requirement of a task node
InformationSpaceBindings = dict[str,tuple[InformationSpaceRequirement,InformationSpace|None]]

def resolve_info_space_bindings(models: ModelSet, node: TaskNode) -> InformationSpaceBindings:
    """Find the information spaces to which the bindings refer indirectly"""
    parent_bindings = None

    if isinstance(node,TaskInstance):
        required = node.get_definition().info_space_requirements
    elif isinstance(node,ImplicitTaskInstance):
        required = node.template.get_definition().info_space_requirements
    elif isinstance(node,Task) or isinstance(node,TaskDefinition):
        required = node.info_space_requirements
    elif isinstance(node,ImplicitTask) or isinstance(node,ImplicitTaskDefinition):
        required = node.template.info_space_requirements
    else:
        return {}

    resolved = {}
    model_id =  node.model.id
    
    for req in required:
        req_name = req.name
        req_binding = req.binding
        if isinstance(node,TaskInstance):
             for irb in node.info_space_bindings:
                if irb.name == req_name:
                    req_binding = irb.binding
                    break

        resolved[req_name] = (req,None)
        if req_binding is not None:
            #Check global space
            if models.info_space_exists(req_binding, model_id):
                resolved[req_name] = (req,models.get_info_space_by_id(req_binding, model_id))
            else:
                if parent_bindings is None and isinstance(node.parent,TaskNode):
                    parent_bindings = resolve_info_space_bindings(models, node.parent)
                if parent_bindings is not None and req_binding in parent_bindings:
                    resolved[req_name] = (req,parent_bindings[req_binding][1])
    return resolved

TriggerBindings = list[tuple[Trigger,InformationSpace|None]]

def resolve_trigger_bindings(models: ModelSet, node: TaskNode) -> TriggerBindings:
    
    if node.parent is None:
        return []
    
    #Only resolve for taskdefinitions
    if not isinstance(node,TaskDefinition) or isinstance(node,ImplicitTaskDefinition):
        return []
    
    #Top-level instances
    resolved = []
    model_id = node.model.id
    if isinstance(node.parent,Model):
        info_spaces = models.list_info_spaces(model_id)
        for trigger in node.triggers:
            if trigger.reference in info_spaces:
                resolved.append((trigger,models.get_info_space_by_id(trigger.reference,model_id)))
            else:
                resolved.append((trigger,None))
    else:
        bound_spaces = resolve_info_space_bindings(models,node.parent)
        for trigger in node.triggers:
            if trigger.reference in bound_spaces:
                resolved.append((trigger,bound_spaces[trigger.reference][1]))
            else:
                resolved.append((trigger,None))
    return resolved

def resolve_parameter_value(node: Node, field_name: str) -> Any | None:
   
    while not isinstance(node,Model):
        if isinstance(node,TaskInstance) and node.parameter is not None and field_name in node.parameter:
            return node.parameter[field_name]
        if isinstance(node,ImplicitTaskInstance) and node.template.parameter is not None and field_name in node.template.parameter:
            return node.template.parameter[field_name]
        
        assert node.parent is not None
        node = node.parent

    return None

def resolve_indirect_imports(models: ModelSet, model_id: ModelID) -> list[ModelID]:
    """Find all models that are indirectly imported from a given model"""
    todo = {model_id}
    done = {model_id}
    while todo:
        model = models.get_model_by_id(todo.pop())
        done.add(model.id)
        for import_def in model.imports:
            if import_def.reference not in done:
                todo.add(import_def.reference)
       
    return list(sorted(done))


def collect_atomic_task_nodes(model: Model) -> list[TaskNode]:
    """Collect all explicit or implicit tasks that are not broken down into sub-tasks"""
   
    def collect(node: TaskNode,
                result: list[TaskNode]):
         
        sub_nodes = [sub_node for sub_node in node.complete_nodes if isinstance(sub_node,TaskNode)]
        if sub_nodes:
            for sub_node in sub_nodes:
                collect(sub_node,result)
        else:
            result.append(node)

    result = []
    for node in (sub_node for sub_node in model.complete_nodes if isinstance(sub_node,TaskNode)):
        collect(node,result)
    return result

#### Specific queries on the network model relevant for execution

def list_concrete_atomic_tasks(model_set: ModelSet) -> list[TaskID]:
    """List all explicit or implicit tasks and task instances that are not decomposed into sub tasks"""
    
    concrete = []
    for model_id in model_set.list_all_models():
        model = model_set.get_model_by_id(model_id)
        atomic_nodes = collect_atomic_task_nodes(model)
        for node in atomic_nodes:
            if (isinstance(node,Task) or isinstance(node,TaskInstance) or isinstance(node,ImplicitTask) or isinstance(node,ImplicitTaskInstance)) and node.is_concrete():
                concrete.append(node.node_id)

    return concrete

def list_concrete_task_definitions(model_set: ModelSet, model_id: ModelID) -> list[TaskID]:
    """List all explicit or implicit tasks definitions in concrete tasks"""
    
    def collect(node: TaskNode, result: list[TaskID]):
        
        if isinstance(node,TaskDefinition) or isinstance(node,ImplicitTaskDefinition):
            result.append(node.node_id)
            return
        
        for sub_node in node.complete_nodes:
            if isinstance(sub_node,TaskNode):
                collect(sub_node,result)
        
    result = []
    for model_id in model_set.list_imported_models(model_id):
        if not model_set.model_exists(model_id):
            continue
        model = model_set.get_model_by_id(model_id)
        for node in model.complete_nodes:
            if isinstance(node,TaskNode):
                collect(node,result)
        
    return result

def list_actor_affiliations(model_set: ModelSet, model_id: ModelID, actor_id: ActorID) -> list[ActorID]:
    """List all organizations, groups or teams that an actor is directly or indirectly a member of"""
    #Basic breadth-first search
    all_actors = [model_set.get_actor_by_id(a,model_id) for a in model_set.list_actors(model_id)]
    orgs = []
    todo = [actor_id]
    while todo:
        cur_id = todo.pop(0)
        cur_actor = model_set.get_actor_by_id(actor_id,model_id)
        
        orgs.append(cur_id)

        for group in cur_actor.groups:
            if group not in orgs and group not in todo:
                todo.append(group)
        for actor in all_actors:
            if cur_id in actor.members and actor.node_id not in orgs and actor.node_id not in todo:
                todo.append(actor.node_id)
      
    return orgs

def list_affiliated_actors(models: ModelSet, model_id: ModelID, actor_name: ActorID, indirect = False) -> list[ActorID]:
    """Return all actors affiliated with a given actor"""

    #TODO: Include indirect affiliations
    #FIXME: Use the modelset to determine the groups

    return [a.name for a in (models.get_actor_by_id(id) for id in models.list_actors(model_id)) if actor_name in a.groups]


def list_actor_locations(model_set: ModelSet, actor_id: ActorID) -> list[LocationID]:
    """List all locations, that an actor is directly or indirectly in"""
    #TODO: Include indirect locations, similar to affiliations
    return model_set.get_actor_by_id(actor_id).locations

def apply_actor_constraints(model_set: ModelSet, model_id: ModelID, actor_id: ActorID, task_ids: list[TaskID]) -> list[TaskID]:
    """Constrain the list of task ids for the given actor"""

    actor_orgs = list_actor_affiliations(model_set, model_id, actor_id)
    actor_tasks = []
    for task_id in task_ids:
        allowed = True
        cur_task = model_set.get_task_by_id(task_id)
        while allowed and cur_task is not None:
            for_actor = cur_task.for_actor
            if for_actor is not None and for_actor not in actor_orgs:
                allowed = False
            else:
                cur_task = cur_task.parent if isinstance(cur_task.parent,TaskNode) else None
        if allowed:
            actor_tasks.append(task_id)

    return actor_tasks

def collect_actor_concrete_atomic_tasks(model_set: ModelSet, model_id: ModelID, actor_id: ActorID) -> list[TaskID]:
    """List all concrete tasks that an actor can work on considering actor and location constraints"""
    concrete_tasks = list_concrete_atomic_tasks(model_set)
    actor_tasks = apply_actor_constraints(model_set, model_id, actor_id, concrete_tasks)
    return actor_tasks

def collect_actor_concrete_task_definitions(model_set: ModelSet, model_id: ModelID, actor_id: ActorID) -> list[TaskID]:
    """List all concrete tasks that an actor can work on considering actor and location constraints"""
    concrete_defs = list_concrete_task_definitions(model_set, model_id)
    actor_defs = apply_actor_constraints(model_set, model_id, actor_id, concrete_defs)
    return actor_defs

def collect_actor_information_spaces(model_set: ModelSet, model_id: ModelID, actor_id: ActorID) -> list[InformationSpaceID]:
    """List all information spaces that are available to an actor considering actor and location constraints"""
    info_spaces = model_set.list_info_spaces(model_id)
    
    actor_locations = list_actor_locations(model_set,actor_id)
    actor_affiliations = list_actor_affiliations(model_set, model_id,actor_id)

    actor_info_spaces = []
    for ifs_id in info_spaces:
        ifs = model_set.get_info_space_by_id(ifs_id)
        at_location = ifs.at_location
        for_actor = ifs.for_actor
        if (at_location is None or at_location in actor_locations) and \
            (for_actor is None or for_actor in actor_affiliations):
            actor_info_spaces.append(ifs_id)
    return actor_info_spaces


def recent_records(info_space: InformationSpace, time: int, window: int = 1):
    return [record for record in info_space.records
            if record.create_time is not None and record.create_time >= (time - window)]


def indexed_fields(info_space: InformationSpace) -> dict[Any,dict[Any,Any]]:
    index = {}
    key = info_space.key_field
    for record in info_space.records:
        if key is None:
            index[record.sequence_number] = record.fields
        else:
            index[record.fields[key]] = record.fields
        
    return index

def actors_at_location(model_set: ModelSet, model_id: ModelID, location_id: LocationID) -> list[ActorID]:
    #TODO consider indirect locations and actor relationships
    at_location = []
    for actor_id in model_set.list_actors(model_id):
        if location_id in model_set.get_actor_by_id(actor_id).locations:
            at_location.append(actor_id)
    return at_location


def instance_exists(model_set: ModelSet, task_id: TaskID, parameter: dict[str,Any]) -> bool:
    """Check if a task instance with the given parameter exists"""
    task_def = model_set.get_task_by_id(task_id)

    if not (isinstance(task_def,TaskDefinition) or isinstance(task_def,ImplicitTaskDefinition)):
        raise ValueError(f'{task_id} does not refer to a task definition')
    
    for instance in task_def.get_instances():
        if instance.parameter == parameter:
            return True
    return False

def next_instance_sequence(model_set: ModelSet, task_id: TaskID):
    task_def = model_set.get_task_by_id(task_id)

    if not (isinstance(task_def,TaskDefinition) or isinstance(task_def,ImplicitTaskDefinition)):
        raise ValueError(f'{task_id} does not refer to a task definition')

    existing = [node.sequence for node in task_def.parent.nodes if isinstance(node,TaskInstance) and node.name == task_def.name]
    return max(existing) + 1 if existing else 1

def list_organizations(models: ModelSet, model_id: ModelID) -> list[ActorID]:
    #Actors who are listed as group or contain members are by definition organizations
    organizations = set()
    for actor_id in models.list_actors(model_id):
        actor = models.get_actor_by_id(actor_id)
        if actor.members:
            organizations.add(actor.node_id)
        organizations.update(actor.groups)
    return sorted(organizations)
    
def list_individuals(models: ModelSet, model_id: ModelID) -> list[ActorID]:
    #Individuals are actors that are not an organization
    organizations = set(list_organizations(models,model_id))
    individuals = set(models.list_actors(model_id)).difference(organizations)
    return sorted(individuals)

def list_performers(model: Model, actor: ActorID) -> set[ActorID]:
    """Return the names of all actors that (indirectly) work for this actor, including itself"""
    
    def performer_set(model: Model, current: set[ActorID]) -> set[ActorID]:
        """Return the names of all actors that (indirectly) work for these actors, including themselves"""
        check_queue = list(current)
        workers = set(current)
        while check_queue:
            check = check_queue.pop(0)
            for actor in model.actors:
                if check in actor.groups:
                    workers.add(actor.name)
                    check_queue.append(actor.name)
        return workers
    
    return performer_set(model, {actor})
