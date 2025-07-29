from ..models.execution import Scenario, ScenarioInformationEvent, ScenarioTaskInitiateEvent, ScenarioJoinGroupEvent, ScenarioLeaveGroupEvent
from ..models.execution import ScenarioEnterLocationEvent, ScenarioLeaveLocationEvent, ScenarioMoveEvent
from ..models.identifier import ScenarioID

import pathlib
import csv, json

def scenario_to_csv_file(scenario: Scenario, path: pathlib.Path | str) -> None:
    """Writes a scenario as a CSV formatted file"""
    if isinstance(path,str):
        path = pathlib.Path(path)

    with open(path,'w') as f:
        writer = csv.writer(f)
        writer.writerow(["time","event","actor","node","data","context","for-actor"])
        writer.writerow([0,"start",None,scenario.model,None,None,None])

        for event in scenario.events:
            match event:
                case ScenarioInformationEvent():
                    data = json.dumps(event.fields) if event.fields is not None else None
                    writer.writerow([event.time,"info",event.actor,event.information_space,data,event.task,None])
                case ScenarioTaskInitiateEvent():
                    parameter = json.dumps(event.parameter)
                    writer.writerow([event.time,"initiate",event.actor,event.task_definition,parameter,event.trigger,event.for_actor])
                case ScenarioJoinGroupEvent():
                    writer.writerow([event.time,"join-group",event.actor,event.group,None,None,None])
                case ScenarioLeaveGroupEvent():
                    writer.writerow([event.time,"leave-group",event.actor,event.group,None,None,None])
                case ScenarioEnterLocationEvent():
                    writer.writerow([event.time,"enter-location",event.actor,event.location,None,None,None])
                case ScenarioLeaveLocationEvent():
                    writer.writerow([event.time,"leave-location",event.actor,event.location,None,None,None])
                case ScenarioMoveEvent():
                    writer.writerow([event.time,"move",event.actor,event.location,None,None,None])