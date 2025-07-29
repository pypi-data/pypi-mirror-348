from ..models.execution import Scenario, ScenarioEvent, ScenarioInformationEvent, ScenarioTaskInitiateEvent, ScenarioJoinGroupEvent, ScenarioLeaveGroupEvent
from ..models.execution import ScenarioEnterLocationEvent, ScenarioLeaveLocationEvent, ScenarioMoveEvent
from ..models.identifier import ScenarioID

import pathlib
import csv, json

def scenario_from_csv_file(scenario_id: ScenarioID, path: str | pathlib.Path) -> Scenario:
    if isinstance(path,str):
        path = pathlib.Path(path)
    
    with open(path,'r') as f:
        reader = csv.reader(f)
        events: list[ScenarioEvent] = []
        model_id = None

        #Check header
        if next(reader) != ["time","event","actor","node","data","context","for-actor"]:
            raise ValueError("Invalid file header")

        #Get start event
        event = next(reader)
        if len(event) != 7 and event[1] != "start":
            raise ValueError("Invalid start event")
        
        model_id = event[3]

        #Read additional events
        for event in reader:
            match event:
                case [time,"info",actor,node,data,context,_]:
                    events.append(ScenarioInformationEvent(
                        int(time),actor,node,json.loads(data),context))
                case [time,"initiate",actor,node,data,context,for_actor]:
                    events.append(ScenarioTaskInitiateEvent(
                        int(time),actor,node,json.loads(data),context if context != '' else None,for_actor if for_actor != '' else None))
                case [time,"join-group",actor,node,_,_,_]:
                    events.append(ScenarioJoinGroupEvent(
                        int(time),actor,node))
                case [time,"leave-group",actor,node,_,_,_]:
                    events.append(ScenarioLeaveGroupEvent(
                        int(time),actor,node))
                case [time,"enter-location",actor,node,_,_,_]:
                    events.append(ScenarioEnterLocationEvent(
                        int(time),actor,node))
                case [time,"leave-location",actor,node,_,_,_]:
                    events.append(ScenarioLeaveLocationEvent(
                        int(time),actor,node))
                case [time,"move",actor,node,_,_,_]:
                    events.append(ScenarioMoveEvent(
                        int(time),actor,node))
                case _:
                    raise ValueError(f"Unexpected event {event}")

    return Scenario(scenario_id,model_id,events)