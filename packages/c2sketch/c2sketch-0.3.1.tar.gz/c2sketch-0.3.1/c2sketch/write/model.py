"""Represent models in c2sketch's own concrete syntax"""
from __future__  import annotations

from c2sketch.models import (Node, Model, Import, Attribute, Constraint, Actor, ActorGroup, ActorMember, ActorLocation, Location, LocationGroup, LocationMember,
                               InformationSpaceRequirement, InformationSpaceBinding,
                               InformationSpace, FieldMode, KeyLimit, AgeLimit, Record, RecordType, RecordTypeField,
                               Task, TaskReference, Trigger, TaskDefinition, TaskInstance )
from typing import Any
import pathlib
import os

def model_node_to_c2s_str(node: Node) -> str:
    
    def indent(text: str) -> str:
        return os.linesep.join(f'    {line}' for line in text.splitlines())
    def nodes_str(nodes: list[Node]) -> str:
        return f':{os.linesep}{os.linesep.join(indent(model_node_to_c2s_str(node)) for node in nodes)}' if nodes else ''
    def fields_str(fields: dict[str,Any]) -> str:
        fields_str = [f'{key} = "{value}"' for key, value in fields.items()]
        return f'{{{", ".join(fields_str)}}}'

    match node:
        case Model():
            return os.linesep.join(model_node_to_c2s_str(child_node) for child_node in node.nodes)
        case Import():
            return f'import {node.reference}'
        case Attribute():
            if os.linesep in node.value:
                return f'@{node.name}:{os.linesep}{indent(node.value)}'
            else:
                return f'@{node.name} "{node.value}"'
        case Constraint():
            return f'!{node.name} {node.value}'    
        case Actor():
            return f'actor {node.name}{nodes_str(node.nodes)}'
        case ActorMember():
            return f'member {node.actor_id}'
        case ActorGroup():
            return f'group {node.group_id}'
        case ActorLocation():
            return f'at-location {node.location_id}'
        case Location():
            return f'location {node.name}{nodes_str(node.nodes)}'
        case LocationMember():
            return f'member {node.location_id}'
        case LocationGroup():
            return f'group {node.group_id}'
        case Task():
            return f'task {node.name}{nodes_str(node.nodes)}'
        case TaskReference():
            parameter_str = '' if node.parameter is None else f' {fields_str(node.parameter)}'
            return f'task-ref {node.reference}{parameter_str}'
        case Trigger():
            return f'trigger {node.reference}'
        case InformationSpaceRequirement(): 
            if node.read and node.write:
                direction_str = '<-> '
            elif node.read:
                direction_str = '<- '
            elif node.write:
                direction_str = '-> '
            else:
                direction_str = ''
            type_str = '' if node.type is None else f' [{node.type}]'
            binding_str = '' if node.binding is None else f' = {node.binding}'
            return f'info-req {direction_str}{node.name}{type_str}{binding_str}'  
        case TaskDefinition():
            type_str = '' if node.parameter_type is None else f'[{node.parameter_type}]'
            return f'task-def {node.name}{type_str}{nodes_str(node.nodes)}'
        case TaskInstance() if node.parameter is not None:
            parameter_str = '' if node.parameter is None else f' {fields_str(node.parameter)}'
            return f'task-instance {node.name}{parameter_str}{nodes_str(node.nodes)}'
        case InformationSpaceBinding():
            return f'info-req {node.name} = {node.binding}'
        case InformationSpace():
            type_str = '' if node.type is None else f' [{node.type}]'
            return f'info-space {node.name}{type_str}{nodes_str(node.nodes)}'
        case FieldMode():
            return f'field-mode {node.field_name} {node.mode}'
        case KeyLimit():
            return f'key-limit {node.limit}'
        case AgeLimit():
            return f'age-limit {node.limit}'
        case Record():
            return f'record {fields_str(node.fields)}'
        case RecordType():
            return f'record-type {node.name}{nodes_str(node.nodes)}'
        case RecordTypeField():
            type_str = '' if node.type is None else f' [{node.type}]'
            return f'field {node.name}{type_str}'
    return ''

def model_to_c2s_str(model: Model, reformat: bool = False) -> str:
    if model.source and not reformat:
        return os.linesep.join(model.source)
    return model_node_to_c2s_str(model)

def model_to_c2s_file(model: Model, path: str | pathlib.Path) -> None:
    
    if isinstance(path,str):
        path = pathlib.Path(path)

    path.write_text(model_to_c2s_str(model))