from __future__ import annotations
from c2sketch.models import *
from c2sketch.execute import plugins
from dataclasses import dataclass, field
from copy import deepcopy
import datetime

__all__ = ('ExecutionState',)

class ExecutionState:
    """Execution state during execution of a scenario
    
    Even though the current set of tasks and information spaces at a moment in time
    can be deterministically computed from a scenario it is too expensive during exection.
    This cache keeps the current state of a scenario readily available.
    """

    init_models: ModelSet #Initially configured models to allow reset
    init_events: list[ScenarioEvent] 

    main_model: ModelID

    models: ModelSet
    events: list[ScenarioEvent]

    time: int = 0 #Discrete time step, resolution can be different for different models
    
    #Options
    playback: bool = False #When the time is increased, events from the scenario are applied
    record: bool = False #New events are inserted into the scenario

    agents: dict[ActorID,plugins.Agent]
    max_ids: dict[str,int]
    event_index: int
    ifs_indexes: dict[InformationSpaceID,dict[str,Record]]

    def __init__(self, models: ModelSet, scenario: Scenario, playback: bool = False, record: bool = False):
        self.init_models = deepcopy(models)
        self.init_events = deepcopy(scenario.events)

        self.models = deepcopy(self.init_models)
        self.main_model = scenario.model

        self.events = deepcopy(scenario.events)
        self.time = 0
        
        self.playback = playback
        self.record = record

        self.agents = {}
        self.max_ids = {}
        self.event_index = 0
        self.ifs_indexes  = {}

        #Build initial info space indexes
        for ifs_id in self.models.list_info_spaces(self.main_model):
            ifs = self.models.get_info_space_by_id(ifs_id,self.main_model)
            if ifs.key_field is not None:
                index = {}
                key_field = ifs.key_field
                for ifs_record in ifs.records:
                    index[ifs_record.fields[key_field]] = ifs_record
                self.ifs_indexes[ifs_id] = index

    def list_agents(self) -> list[ActorID]:
        agents = []
        for actor_id in self.models.list_actors(self.main_model):
            actor = self.models.get_actor_by_id(actor_id)
            
            if actor.get_attribute('agent-type') is not None:
                agents.append(actor_id)
        return agents
    
    def list_active_agents(self) -> list[ActorID]:
        return list(self.agents.keys())
    
    def agent_status(self) -> dict[ActorID,bool]:
        return {agent_id: agent_id in self.agents for agent_id in self.list_agents()}
    
    def start_agents(self, loader: plugins.PluginLoader):
        for actor_id in self.models.list_actors(self.main_model):
            self.start_agent(loader,actor_id)
        
    def start_agent(self, loader: plugins.PluginLoader, actor_id: ActorID):
        actor = self.models.get_actor_by_id(actor_id)   
        agent_type_id = actor.get_attribute('agent-type')
        if agent_type_id is not None and actor_id not in self.agents:
            agent_cls = loader.agents[agent_type_id]
            agent = agent_cls()
            agent.start(self.time,actor_id,self.models)
            self.agents[actor_id] = agent

    def stop_agents(self):
        for agent in self.agents.values():
            agent.stop(self.time)

        self.agents.clear()

    def stop_agent(self, actor_id: ActorID):
        if actor_id in self.agents:
            agent = self.agents.pop(actor_id)
            agent.stop(self.time)

    def reset(self):
        self.time = 0
        self.models = deepcopy(self.init_models)
        self.event_index = 0

    def step_time(self):
        """Increase time and apply scenario events, if applicable"""
        self.time += 1

        #Align the event_index and apply events if playback is enabled
        if self.events:
            while self.event_index < len(self.events) and self.events[self.event_index].time <= self.time:
                if self.playback:
                    apply_scenario_event(self.models,self.main_model,self.ifs_indexes,self.events[self.event_index])
                self.event_index += 1

        agent_events = []
        for agent_id in sorted(self.agents.keys()): #Deterministic ordering
            agent = self.agents[agent_id]
            agent_events.extend(agent.interact(self.time,self.models))
        
        if agent_events:
            for event in agent_events:
                self.apply_event(event)
              
    def apply_event(self, event: ScenarioEvent):
        #Apply event to the models and
        #If record is enabled insert the event into the scenario
        apply_scenario_event(self.models,self.main_model,self.ifs_indexes,event)
        if self.record:
            if self.event_index < len(self.events):
                self.events.insert(self.event_index,event)
                self.event_index += 1
            else:
                self.events.append(event)
