"""Generic plugin for generating messages at fixed intervals."""

from c2sketch.execute.plugins import Agent
from c2sketch.models import *

class TimerAgent(Agent):
    def interact(self, time: int, models: ModelSet) -> list[ScenarioEvent]:
        return super().interact(time, models)
    
def config_type():
    return RecordType(None,'clock_feed_config',[
        RecordTypeField('fieldname', 'string'),#Output field name
        RecordTypeField('local', 'string'),#Use local time default is UTC
    ])