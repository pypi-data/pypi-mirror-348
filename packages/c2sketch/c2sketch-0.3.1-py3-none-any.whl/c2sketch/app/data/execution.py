
import asyncio

from toppyt import DataSource, read, write
from copy import deepcopy

from toppyt.datasources import Registration
from toppyt.tasks import Application

from c2sketch.models import *
from c2sketch.execute import ExecutionState

from c2sketch.read.folder import model_set_from_folder
from c2sketch.read.scenario import scenario_from_csv_file
from c2sketch.write.scenario import scenario_to_csv_file

from c2sketch.app.plugins import AppPluginLoader

from typing import Any
from pathlib import Path
from bisect import bisect_left

__all__ = ['ExecutionStore']

class ExecutionStore(DataSource):
    """Database abstraction that manages execution information"""

    model_path: Path
    scenario_path: Path
    plugin_loader: AppPluginLoader

    executions: dict[ScenarioID,ExecutionState]
    timers: dict[ScenarioID,asyncio.Task]

    def __init__(self, model_path: Path, scenario_path: Path, plugin_loader: AppPluginLoader):
        
        self.model_path = model_path
        self.scenario_path = scenario_path
        self.plugin_loader = plugin_loader

        self.executions = {}
        self.timers = {}

        super().__init__()

    def start(self, application: Application):
        return super().start(application)
    
    def register(self, registration: Registration):
        return super().register(registration)
    
    def notify(self, registration):
        match self._method:
            case 'start_agents':
                criterium = lambda method, args, kwargs: method == 'agent_status'
            case 'stop_agents':
                criterium = lambda method, args, kwargs: method == 'agent_status'
            case '_tick_timer':
                criterium = lambda method, args, kwargs: method in ('execution_time','info_space_content','actor_concrete_atomic_tasks')
            case _:
                criterium = lambda method, args, kwargs: True
    
        remaining_readers = []
        if self._readers and self._application is not None:
            for registration, method, args, kwargs in self._readers:
                if criterium(method,args,kwargs):
                    self._application.notify_session(registration.session, registration.task)
                else:
                    remaining_readers.append((registration, method, args, kwargs))
        self._readers = remaining_readers

    @read
    async def list_scenarios(self) -> list[ScenarioID]:
        scenario_ids = []
        for item in self.scenario_path.iterdir():
            if item.name.endswith('.csv'):
                scenario_ids.append(item.stem) 
        return scenario_ids
    
    @read
    async def list_executions(self) -> list[ScenarioID]:
        return sorted(self.executions.keys())

    @write
    async def create_execution(self, scenario_id: ScenarioID, model_id: ModelID) -> ScenarioID:

        #Construct empty scenario
        scenario = Scenario(scenario_id,model_id)
        models = model_set_from_folder(self.model_path, scenario.model)

        #Construct execution state
        self.executions[scenario_id] = ExecutionState(models,scenario)
    
        return scenario_id
    
    @write
    async def delete_execution(self, scenario_id: ScenarioID):
        if scenario_id not in self.executions:
            return
        
        if scenario_id in self.timers:
            timer = self.timers.pop(scenario_id)
            timer.cancel()

        self.executions.pop(scenario_id)

    @write
    async def load_execution(self, scenario_id: ScenarioID) -> None:
        
        if scenario_id in self.executions:
            return

        scenario = scenario_from_csv_file(scenario_id,self.scenario_path.joinpath(f'{scenario_id}.csv'))
        models = model_set_from_folder(self.model_path, scenario.model)
        
        self.executions[scenario_id] = ExecutionState(models,scenario)

    async def save_execution(self, scenario_id: ScenarioID, save_id: ScenarioID) -> None:
        scenario = Scenario(save_id, self.executions[scenario_id].main_model, self.executions[scenario_id].events)
        scenario_to_csv_file(scenario,self.scenario_path.joinpath(f'{save_id}.csv'))

    @read
    async def execution_exists(self, scenario_id: ScenarioID) -> bool:
        return scenario_id in self.executions
    
    @read
    async def execution_time(self, scenario_id: ScenarioID) -> int:
        return self.executions[scenario_id].time

    @read
    async def execution_options(self, scenario_id: ScenarioID) -> dict[str,bool]:
        execution = self.executions[scenario_id]
        return {"playback":execution.playback, "record": execution.record}

    @write
    async def set_execution_options(self,scenario_id: ScenarioID, options: dict[str,bool]) -> None:
        execution = self.executions[scenario_id]

        execution.playback = options.get("playback",False)
        execution.record = options.get("record",False)

    @read
    async def execution_model(self, scenario_id: ScenarioID) -> tuple[ModelID,ModelSet]:
        execution = self.executions[scenario_id]
        return (execution.main_model,execution.models)

    @read
    async def num_actors(self, scenario_id: ScenarioID) -> int:
        execution = self.executions[scenario_id]
        return len(execution.models.list_actors(execution.main_model))
    
    @read
    async def list_actors(self, scenario_id: ScenarioID, limit: int | None = None, offset: int = 0) -> list[tuple[ActorID,str]]:
        """List all actor id's and titles"""
        result = []
        execution = self.executions[scenario_id]
        for actor_id in execution.models.list_actors(execution.main_model):
            actor_label = execution.models.get_actor_by_id(actor_id,execution.main_model).label
            result.append((actor_id,actor_label))
        if limit is None:
            return result
        else:
            return result[offset:offset+limit]
    
    @read
    async def list_locations(self, scenario_id: ScenarioID) -> list[tuple[LocationID,str]]:
        """List all actor id's and titles"""
        result = []
        execution = self.executions[scenario_id]
        for location_id in execution.models.list_locations(execution.main_model):
            location_label = execution.models.get_location_by_id(location_id,execution.main_model).label
            result.append((location_id,location_label))
        return result

    @read
    async def list_info_spaces(self, scenario_id: ScenarioID) -> list[tuple[InformationSpaceID,str]]:
        result = []
        execution = self.executions[scenario_id]
        for ifs_id in execution.models.list_info_spaces(execution.main_model):
            ifs_label = execution.models.get_info_space_by_id(ifs_id,execution.main_model).label
            result.append((ifs_id,ifs_label))
        return result
    
    @read
    async def agent_status(self, scenario_id: ScenarioID) -> dict[ActorID,bool]:
        execution = self.executions[scenario_id]
        return execution.agent_status()

    @read
    async def actor_title(self, scenario_id: ScenarioID, actor_id: ActorID) -> str:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        actor = models.get_actor_by_id(actor_id,model_id)

        return actor.label

    @read
    async def actor_locations(self, scenario_id: ScenarioID, actor_id: ActorID) -> str:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        actor = models.get_actor_by_id(actor_id,model_id)
        locations = actor.locations
        if locations:
            return ", ".join([models.get_location_by_id(location,model_id).label for location in locations])
        else:
            return "-"
    
    @read
    async def actor_groups(self, scenario_id: ScenarioID, actor_id: ActorID) -> list[ActorID]:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        return list_actor_affiliations(models,model_id,actor_id)
    
    @read
    async def actor_concrete_atomic_tasks(self, scenario_id: ScenarioID, actor_id: ActorID) -> list[TaskID]:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        return collect_actor_concrete_atomic_tasks(models, model_id, actor_id)
    
    @read
    async def actor_concrete_task_definitions(self, scenario_id: ScenarioID, actor_id: ActorID) -> list[TaskID]:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        return collect_actor_concrete_task_definitions(models, model_id, actor_id)

    @read
    async def actor_location_information_spaces(self, scenario_id: ScenarioID, actor_id: ActorID) -> list[InformationSpaceID]:
        models = self.executions[scenario_id].models
        model_id = self.executions[scenario_id].main_model
        return collect_actor_information_spaces(models, model_id, actor_id)

    @read
    async def task_information_spaces(self, scenario_id: ScenarioID, task_id: TaskID) -> list[InformationSpaceID]:
        models = self.executions[scenario_id].models
        task = models.get_task_by_id(task_id)
        bindings = resolve_info_space_bindings(models,task)
        return [ifs.node_id for req, ifs in bindings.values() if ifs is not None]

    @read
    async def info_space_type(self, scenario_id, ifs_id) -> RecordType | None:
        models = self.executions[scenario_id].models
        model_id = local_id_from_global_id(ifs_id)[1]
        ifs = models.get_info_space_by_id(ifs_id)
        if ifs.type is None:
            return None
        
        record_type = models.get_record_type_by_id(ifs.type,model_id) 
        return record_type
    
    @read
    async def info_space_content(self, scenario_id: ScenarioID, ifs_id: InformationSpaceID) -> list[Record]:
        models = self.executions[scenario_id].models
        ifs = models.get_info_space_by_id(ifs_id)
        return ifs.records
    
    @read
    async def info_space_graphic_plugin(self, scenario_id: ScenarioID, ifs_id: InformationSpaceID) -> str | None:
        models = self.executions[scenario_id].models
        ifs = models.get_info_space_by_id(ifs_id)
        return ifs.get_attribute("graphic-type")
    
    @read
    async def task_definition_parameter_type(self, scenario_id: ScenarioID, task_id: TaskID) -> RecordType | None:
        models = self.executions[scenario_id].models
        model_id = local_id_from_global_id(task_id)[1]
        task_def = models.get_task_by_id(task_id, model_id)
        if not isinstance(task_def,TaskDefinition | ImplicitTaskDefinition):
            return None
        if task_def.parameter_type is None:
            return None
        
        record_type = models.get_record_type_by_id(task_def.parameter_type,model_id) 
        return record_type

    @write
    async def start_agent(self, scenario_id: ScenarioID, actor_id: ActorID) -> None:
        self.executions[scenario_id].start_agent(self.plugin_loader,actor_id)
    @write
    async def start_agents(self, scenario_id: ScenarioID, actor_ids: list[ActorID]) -> None:
        for actor_id in actor_ids:
            self.executions[scenario_id].start_agent(self.plugin_loader,actor_id)
    @write
    async def start_all_agents(self, scenario_id: ScenarioID) -> None:
        self.executions[scenario_id].start_agents(self.plugin_loader)
     
    @write
    async def stop_agent(self, scenario_id: ScenarioID, actor_id: ActorID) -> None:
        self.executions[scenario_id].stop_agent(actor_id)
    @write
    async def stop_agents(self, scenario_id: ScenarioID, actor_ids: list[ActorID]) -> None:
        for actor_id in actor_ids:
            self.executions[scenario_id].stop_agent(actor_id)
    @write
    async def stop_all_agents(self, scenario_id: ScenarioID) -> None:
        self.executions[scenario_id].stop_agents()

    @write
    async def reset_execution(self, scenario_id: ScenarioID) -> None:
        self.executions[scenario_id].reset()

    @write
    async def step_timer(self, scenario_id: ScenarioID) -> None:
        self.executions[scenario_id].step_time()
        
    @write
    async def start_timer(self, scenario_id: ScenarioID) -> None:
        if scenario_id not in self.timers:
            self.timers[scenario_id] = asyncio.create_task(self._tick_timer(scenario_id))
    
    async def _tick_timer(self, scenario_id: ScenarioID) -> None:
        while True:
            self.executions[scenario_id].step_time()
            self._method = '_tick_timer'
            self.notify(None)
            await asyncio.sleep(1)
            
    @write
    async def stop_timer(self, scenario_id: ScenarioID) -> None:
        if scenario_id in self.timers:
            timer = self.timers.pop(scenario_id)
            timer.cancel()
     
    @read
    async def num_events(self, scenario_id: ScenarioID) -> int:
        return len(self.executions[scenario_id].events)
    
    @read
    async def list_events(self, scenario_id: ScenarioID, limit: int | None = None, offset: int = 0) -> list[tuple[int,ScenarioEvent]]:
        """List all recorded events"""
        execution = self.executions[scenario_id]
        if limit is not None:
            return list(enumerate(execution.events[offset:offset+limit],offset))
        else:
            return list(enumerate(execution.events))
    
    @read
    async def get_event(self, scenario_id: ScenarioID, index: int) -> ScenarioEvent:
        execution = self.executions[scenario_id]
        return execution.events[index]
    
    @write
    async def insert_event(self, scenario_id: ScenarioID, event: ScenarioEvent):
        execution = self.executions[scenario_id]
        
        index = bisect_left(execution.events,event.time, key=lambda e: e.time)
        execution.events.insert(index,event)

    @write
    async def update_event(self, scenario_id: ScenarioID, index: int, event: ScenarioEvent):
        execution = self.executions[scenario_id]
        
        if execution.events[index].time == event.time:
            execution.events[index] = event
        else:
            execution.events.pop(index)
            index = bisect_left(execution.events,event, key=lambda e: e.time)
            execution.events.insert(index,event)

    @write
    async def delete_event(self, scenario_id: ScenarioID, index: int):
        execution = self.executions[scenario_id]
        execution.events.pop(index)

    @write
    async def delete_events(self, scenario_id: ScenarioID, indexes: list[int]):
        execution = self.executions[scenario_id]
        events = [event for index, event in enumerate(execution.events) if index not in indexes]
        execution.events = events
        
    @write
    async def emit_information_event(self, scenario_id: ScenarioID, actor_id: ActorID, ifs_id: InformationSpaceID, fields: dict[str,Any], task_id: TaskID | None = None):
        execution = self.executions[scenario_id]
        event = ScenarioInformationEvent(
            time=execution.time, actor = actor_id, information_space = ifs_id,
            fields = deepcopy(fields),task = task_id
        )
        execution.apply_event(event)

    @write
    async def emit_task_initiate_event(self,  scenario_id: ScenarioID, actor_id: ActorID, task_id: TaskID, parameter: dict[str,Any], trigger: InformationSpaceID | None = None, for_actor: ActorID | None = None):
        execution = self.executions[scenario_id]
        event = ScenarioTaskInitiateEvent(
            time = execution.time, actor = actor_id, task_definition = task_id, parameter = parameter, trigger = trigger, for_actor = for_actor
        )
        execution.apply_event(event)
    
    @write
    async def emit_move_event(self, scenario_id: ScenarioID, actor_id: ActorID, location_id: LocationID):
        execution = self.executions[scenario_id]
        event = ScenarioMoveEvent(execution.time, actor_id, location_id)
        execution.apply_event(event)

    @write
    async def emit_join_group_event(self, scenario_id: ScenarioID, actor_id: ActorID, group_id: ActorID):
        execution = self.executions[scenario_id]
        event = ScenarioJoinGroupEvent(execution.time, actor_id, group_id)
        execution.apply_event(event)
    
    @write
    async def emit_leave_group_event(self, scenario_id: ScenarioID, actor_id: ActorID, group_id: ActorID):
        execution = self.executions[scenario_id]
        event = ScenarioLeaveGroupEvent(execution.time, actor_id, group_id)
        execution.apply_event(event)

    async def end(self):
        for timer in self.timers.values():
            timer.cancel()
        return await super().end()

