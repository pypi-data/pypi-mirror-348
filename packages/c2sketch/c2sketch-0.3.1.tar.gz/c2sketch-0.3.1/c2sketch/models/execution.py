"""Scenarios and events for dynamic analysis"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Sequence

from .identifier import *
from .structure import Model, Record, TaskDefinition, ImplicitTaskDefinition, TaskInstance, ImplicitTaskInstance, InformationSpace, Constraint
from .structure import Actor, ActorGroup, ActorMember, ActorLocation
from .collection import ModelSet

import copy

__all__ = [
    'Scenario','ScenarioEvent',
    'ScenarioInformationEvent','ScenarioTaskInitiateEvent',
    'ScenarioJoinGroupEvent','ScenarioLeaveGroupEvent',
    'ScenarioEnterLocationEvent','ScenarioLeaveLocationEvent','ScenarioMoveEvent',
    'apply_scenario_event'
]

@dataclass
class Scenario:
    name: ScenarioName
    model: ModelID # The initial network state
    events: list[ScenarioEvent] = field(default_factory=list) # The sequence of events that transform the model over time

    @property
    def label(self) -> str:
        return self.name

@dataclass
class ScenarioInformationEvent:
    """Send information to an information space"""
    time: int
    actor: ActorID 
    information_space: InformationSpaceID
    fields: dict[str,Any]
    task: TaskID | None = None # Task context in which the information was sent, can be unknown

@dataclass
class ScenarioTaskInitiateEvent:
    """Initiate a new task instance"""
    time: int
    actor: ActorID 
    task_definition: TaskID
    parameter: dict[str,Any]
    trigger: InformationSpaceID | None = None
    for_actor: ActorID | None = None

@dataclass
class ScenarioJoinGroupEvent:
    """Actor joins a group/organization"""
    time: int
    actor: ActorID 
    group: ActorID

@dataclass
class ScenarioLeaveGroupEvent:
    """Actor leaves a group/organization"""
    time: int
    actor: ActorID 
    group: ActorID

@dataclass
class ScenarioEnterLocationEvent:
    """Actor adds location to its current set of locations"""
    time: int
    actor: ActorID
    location: LocationID

@dataclass
class ScenarioLeaveLocationEvent:
    """Actor removes location from its current set of locations"""
    time: int
    actor: ActorID
    location: LocationID

@dataclass
class ScenarioMoveEvent:
    """Actor leaves previous location(s) and enters new location"""
    time: int
    actor: ActorID
    location: LocationID

ScenarioEvent = ScenarioInformationEvent | ScenarioTaskInitiateEvent | ScenarioJoinGroupEvent | ScenarioLeaveGroupEvent | ScenarioEnterLocationEvent | ScenarioLeaveLocationEvent | ScenarioMoveEvent

### Application of events to a network to evolve it over time

def apply_scenario_event(model_set: ModelSet, main_model: ModelID, ifs_indexes: dict[InformationSpaceID,dict[str,Record]], event: ScenarioEvent) -> None:
    #TODO: Check if the events are possible given the constraints of the model
    # E.g. Don't accept for information spaces that unreachable from the actor's locations
    # Or when information is sent to an information space, but the actor has no tasks in which
    # the information space is required
    
    match event:
        case ScenarioInformationEvent():
            info_space = model_set.get_info_space_by_id(event.information_space, main_model)
            if not info_space.node_id in ifs_indexes:
                ifs_indexes[info_space.node_id] = {}
            
            create_records(info_space,ifs_indexes[info_space.node_id],
                records=[Record(event.fields,parent=info_space)],
                create_time=event.time,
                create_actor=event.actor
                )
            limit_records(info_space, event.time)
        case ScenarioTaskInitiateEvent():
            definition = model_set.get_task_by_id(event.task_definition, main_model)
            if isinstance(definition,TaskDefinition) or isinstance(definition,ImplicitTaskDefinition):
                create_instance(definition,event.parameter,event.for_actor)
        case ScenarioJoinGroupEvent():
            actor = model_set.get_actor_by_id(event.actor, main_model)
            group = model_set.get_actor_by_id(event.group, main_model)
            join_group(actor,group)
           
        case ScenarioLeaveGroupEvent():
            actor = model_set.get_actor_by_id(event.actor)
            group = model_set.get_actor_by_id(event.group)
            leave_group(actor,group)

        case ScenarioEnterLocationEvent():
            actor = model_set.get_actor_by_id(event.actor)
            enter_location(actor, event.location)
        case ScenarioLeaveLocationEvent():
            actor = model_set.get_actor_by_id(event.actor)
            leave_location(actor,event.location)
        case ScenarioMoveEvent():
            actor = model_set.get_actor_by_id(event.actor)
            set_location(actor,event.location)

def create_records(ifs: InformationSpace, ifs_index: dict[str,Record], records: Sequence[Record],
                create_time: int | None = None,
                create_actor: ActorID | None = None,
                create_location: LocationID | None = None) -> None:
    
    sequence_number = max(r.sequence_number for r in ifs.records) + 1 if ifs.records else 1
    key_field = ifs.key_field
    field_modes = ifs.field_modes

    if key_field is None:
        #Simply append a copy with updated fields
        #Conceptually the sequence_number is used as key, which guarantees exactly one value exist for each key
        for record in records:
            ifs.nodes.append(Record(
                fields = copy.deepcopy(record.fields),
                sequence_number = sequence_number,
                create_time = create_time if create_time is not None else 0,
                create_actor = create_actor,
                create_location = create_location,
                parent = ifs
            ))
            sequence_number += 1
    else:
        for record in records:
            key = record.fields[key_field]
            if key in ifs_index:
                #Update the record based on the modes of the fields
                key_record = ifs_index[key]
                for field, value in record.fields.items():
                    field_mode = field_modes.get(field,'last')
                    if (field_mode == 'last') or \
                        (key not in key_record.fields and field_mode in {'first','min','max'}) or \
                        (field_mode == 'min' and value < key_record.fields[key]) or\
                        (field_mode == 'max' and value > key_record.fields[key]):
                            key_record.fields[field] = value
                        
                key_record.sequence_number = sequence_number
                if create_time is not None:
                    key_record.create_time = create_time
                if create_actor is not None:
                    key_record.create_actor = create_actor
                if create_location is not None:
                    key_record.create_location = create_location
            else:
                #Add a new record
                key_record = Record(
                    fields = copy.deepcopy(record.fields),
                    sequence_number = sequence_number,
                    create_time= create_time if create_time is not None else 0,
                    create_actor = create_actor,
                    create_location = create_location,
                    parent = ifs)
                ifs.nodes.append(key_record)
                ifs_index[key] = key_record
            sequence_number += 1
        
    
def limit_records(ifs: InformationSpace, time: int) -> None:
    #First remove records that are too old
    age_limit = ifs.age_limit
    if age_limit is not None:
        keep_time = time - age_limit
        ifs.nodes = [node for node in ifs.nodes if (node.create_time >= keep_time if isinstance(node,Record) else True)]   
    
    #If there are still too much records, drop the oldest
    key_limit = ifs.key_limit
    if key_limit is not None:
        records = ifs.records
        if len(records) > key_limit:
            for node in sorted(records, key = lambda record: record.create_time)[len(records) - key_limit:]:
                ifs.nodes.remove(node)

def create_instance(task_def: TaskDefinition | ImplicitTaskDefinition, parameter: dict[str,Any], for_actor: ActorID | None = None):
    
    def task_def_create_instance(task_def: TaskDefinition, parameter: dict[str,Any], for_actor: ActorID | None = None):
        assert task_def.parent is not None

        if task_def.parent is None or not (isinstance(task_def.parent,Model) or task_def.parent.is_concrete()):
            raise Exception('Cannot create task instance without a concrete parent task')
        
        existing = [node.sequence for node in task_def.parent.nodes if isinstance(node,TaskInstance) and node.name == task_def.name]
        sequence = max(existing) + 1 if existing else 1
        instance_node = TaskInstance(task_def.name,sequence,parameter=copy.deepcopy(parameter),parent=task_def.parent)
        task_def.parent.nodes.append(instance_node)
        #Initial constraints
        if for_actor is not None:
            instance_node.nodes.append(Constraint('for-actor',for_actor,parent=task_def))

    def implicit_def_create_instance(task_def: ImplicitTaskDefinition, parameter: dict[str,Any], for_actor: ActorID | None = None):
        assert task_def.parent is not None

        if task_def.parent is None or isinstance(task_def.parent,ImplicitTaskDefinition) or not (isinstance(task_def.parent,Model) or task_def.parent.is_concrete()):
            raise Exception('Cannot create task instance without a concrete parent task')
        
        existing = [node.sequence for node in task_def.parent.nodes if (isinstance(node,TaskInstance) or isinstance(node,ImplicitTaskInstance)) and node.name == task_def.name]
        sequence = max(existing) + 1 if existing else 1
        instance_node = TaskInstance(task_def.name,sequence,parameter=copy.deepcopy(parameter),parent=task_def.parent)
        task_def.parent.nodes.append(instance_node)
        #Initial constraints
        if for_actor is not None:
            instance_node.nodes.append(Constraint('for-actor',for_actor,parent=task_def))

    if isinstance(task_def,TaskDefinition):
        return task_def_create_instance(task_def,parameter,for_actor)
    if isinstance(task_def,ImplicitTaskDefinition):
        return implicit_def_create_instance(task_def,parameter,parameter)
    

def join_group(actor: Actor, group: Actor) -> None:
    if group.node_id in actor.groups:
        return
    actor.nodes.append(ActorGroup(group.node_id,parent=actor))

def leave_group(actor: Actor, group: Actor) -> None:
    remove = None
    model_id = actor.model.id
    for i, node in enumerate(actor.nodes):
        if isinstance(node,ActorGroup) and global_id_from_id(node.group_id,model_id) == group.node_id:
            remove = i
            break
    if remove is not None:
        actor.nodes.pop(remove)

    remove = None
    for i, node in enumerate(group.nodes):
        if isinstance(node,ActorMember) and global_id_from_id(node.actor_id,model_id) == actor.node_id:
            remove = i
            break
    if remove is not None:
        group.nodes.pop(remove)

def enter_location(actor: Actor, location: LocationID):
    if location not in actor.locations:
        actor.nodes.append(ActorLocation(location,parent=actor))

def leave_location(actor: Actor, location: LocationID):
    if location in actor.locations:
        actor.nodes = [node for node in actor.nodes if not (isinstance(node,ActorLocation) and node.location_id == location)]

def set_location(actor: Actor, location: LocationID):
    #Naive implementation: remove all location nodes and creates a single new one
    actor.nodes = [node for node in actor.nodes if not isinstance(node,ActorLocation)]
    actor.nodes.append(ActorLocation(location,parent=actor))