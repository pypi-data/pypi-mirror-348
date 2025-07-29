"""Definition of collections of models that facilitate lookup of nodes between models that reference each other"""
from __future__ import annotations

from .identifier import ModelID, NodeID, TaskID, InformationSpaceID, ActorID, LocationID, RecordTypeID, is_local_id, local_id_from_global_id
from .structure import Model, Node, TaskNode, Task, TaskDefinition, TaskInstance, ImplicitTask, ImplicitTaskDefinition, ImplicitTaskInstance, InformationSpace, Actor, Location, RecordType
from dataclasses import dataclass
from pathlib import Path

from typing import Callable

__all__ = ['ModelSet']

@dataclass
class ModelSetEntry:
    model: Model
    origin: Path | None # Track where the model was loaded from

class ModelSet:
    """A related set of models, allowing lookup of references to imported elements."""
    models: dict [ModelID,ModelSetEntry]

    def __init__(self):
        self.models = {}

    def update(self, other: ModelSet):
        self.models.update(other.models)

    def add_model(self, model: Model, origin: Path | None = None):
        self.models[model.id] = ModelSetEntry(model = model, origin = origin)

    def remove_model(self, model_id: ModelID):
        self.models.pop(model_id)

    def list_all_models(self) -> list[ModelID]:
        return list(self.models.keys())

    def list_imported_models(self, model_id: ModelID) -> list[ModelID]:
        models = set()
        todo = {model_id}

        while todo:
            cur_model_id = todo.pop()
            if cur_model_id in models:
                continue #Already processed

            models.add(cur_model_id)
            if cur_model_id in self.models:
                for model_import in self.models[cur_model_id].model.imports:
                    todo.add(model_import.reference)
        return list(models)
    
    def model_exists(self, model_id: ModelID) -> bool:
        return model_id in self.models
    
    def get_model_by_id(self, model_id: ModelID) -> Model:
        if model_id not in self.models:
            raise KeyError(f'{model_id} not in model set')
        
        return self.models[model_id].model

    # List and lookup methods for:
    # - Actors
    # - Tasks (Including Task definitions and Task instances)
    # - Information Spaces
    # - Locations
    # - Record Types

    def list_actors(self, model_id: ModelID, include_imports: bool = True) -> list[ActorID]:
        node_filter = lambda node: isinstance(node,Actor)
        return self._list_nodes(model_id, include_imports, node_filter)
    
    def list_locations(self, model_id: ModelID, include_imports: bool = True) -> list[LocationID]:
        node_filter = lambda node: isinstance(node,Location)
        return self._list_nodes(model_id, include_imports, node_filter)
    
    def list_tasks(self, model_id: ModelID, include_imports: bool = True) -> list[TaskID]:
        node_filter = lambda node: isinstance(node,TaskNode)
        return self._list_nodes(model_id, include_imports, node_filter)
    
    def list_info_spaces(self, model_id: ModelID, include_imports: bool = True) -> list[InformationSpaceID]:
        node_filter = lambda node: isinstance(node,InformationSpace)
        return self._list_nodes(model_id, include_imports, node_filter)
    
    def list_record_types(self, model_id: ModelID, include_imports: bool = True) -> list[RecordTypeID]:
        node_filter = lambda node: isinstance(node,RecordType)
        return self._list_nodes(model_id, include_imports, node_filter)
    
    def _list_nodes(self, model_id: ModelID, include_imports: bool, node_filter: Callable[[Node],bool]) -> list[NodeID]:
        
        def collect(nodes: list[Node],result: list[NodeID]):
            for node in nodes:
                if node_filter(node):
                    result.append(node.node_id)
                collect(node.complete_nodes,result)
        
        result = []
        model_ids = self.list_imported_models(model_id) if include_imports else [model_id]
        for model_id in model_ids:
            if model_id in self.models:
                model = self.models[model_id].model
                collect(model.nodes,result)
        return result        

    def get_actor_by_id(self, actor_id: TaskID, ctx_model_id: ModelID | None = None) -> Actor:
        def node_test(step: str, node: Node) -> bool:
            return isinstance(node,Actor) and node.name == step

        node = self._get_node_by_id(actor_id,ctx_model_id,node_test)
        assert isinstance(node,Actor)
        return node

    def get_location_by_id(self, location_id: LocationID, ctx_model_id: ModelID | None = None) -> Location:
        def node_test(step: str, node: Node) -> bool:
            return isinstance(node,Location) and node.name == step

        node = self._get_node_by_id(location_id,ctx_model_id,node_test)
        assert isinstance(node,Location)
        return node
    
    def get_task_by_id(self, task_id: TaskID, ctx_model_id: ModelID | None = None) -> TaskNode:
        
        def node_test(step: str, node: Node) -> bool:
            if (isinstance(node,Task) or isinstance(node,ImplicitTask)) and node.name == step:
                return True
            if (isinstance(node,TaskDefinition) or isinstance(node,ImplicitTaskDefinition)) and node.name == step:
                return True
            if (isinstance(node,TaskInstance) or isinstance(node,ImplicitTaskInstance)) and '-' in step:
                step_name, step_sequence = step.split('-')
                step_sequence = int(step_sequence)
                if node.name == step_name and node.sequence == step_sequence:
                    return True
            return False
            
        node = self._get_node_by_id(task_id,ctx_model_id,node_test)
        assert isinstance(node,TaskNode)
        return node

    def get_info_space_by_id(self, ifs_id: InformationSpaceID, ctx_model_id: ModelID | None = None) -> InformationSpace:
        def node_test(step: str, node: Node) -> bool:
            return isinstance(node,InformationSpace) and node.name == step

        node = self._get_node_by_id(ifs_id,ctx_model_id,node_test)
        assert isinstance(node,InformationSpace)
        return node

    def get_record_type_by_id(self, type_id: RecordTypeID, ctx_model_id: ModelID | None = None) -> RecordType:
        def node_test(step: str, node: Node) -> bool:
            return isinstance(node,RecordType) and node.name == step

        node = self._get_node_by_id(type_id,ctx_model_id,node_test)
        assert isinstance(node,RecordType)
        return node

    def _get_node_by_id(self, node_id: NodeID, ctx_model_id: ModelID | None, node_test: Callable[[str,Node],bool]) -> Node:
        if is_local_id(node_id):
            if ctx_model_id is None:
                raise ValueError(f'No model id given for local identifier {node_id}')
            
            local_id, model_id = node_id, ctx_model_id
        else:
            local_id, model_id = local_id_from_global_id(node_id)

        model = self.models[model_id].model
        current_node = model
        for step in local_id.split('.'):
            for node in current_node.complete_nodes:
                if node_test(step,node):
                    current_node = node
                    break
            else:
                raise KeyError(f'{node_id} does not exist')

        return current_node

    def actor_exists(self, actor_id: ActorID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_actor_by_id(actor_id, ctx_model_id)
            return True
        except KeyError:
            return False
    
    def location_exists(self, location_id: LocationID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_location_by_id(location_id, ctx_model_id)
            return True
        except KeyError:
            return False
    
    def task_exists(self, task_id: TaskID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_task_by_id(task_id, ctx_model_id)
            return True
        except KeyError:
            return False
    def task_definition_exists(self, task_id: TaskID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_task_by_id(task_id, ctx_model_id)
            return True
        except KeyError:
            return False
    def task_instance_exists(self, task_id: TaskID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_task_by_id(task_id, ctx_model_id)
            return True
        except KeyError:
            return False
       
    def info_space_exists(self, ifs_id: InformationSpaceID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_info_space_by_id(ifs_id, ctx_model_id)
            return True
        except KeyError:
            return False
       
    def record_type_exists(self, type_id: RecordTypeID, ctx_model_id: ModelID | None = None) -> bool:
        try:
            self.get_record_type_by_id(type_id, ctx_model_id)
            return True
        except KeyError:
            return False