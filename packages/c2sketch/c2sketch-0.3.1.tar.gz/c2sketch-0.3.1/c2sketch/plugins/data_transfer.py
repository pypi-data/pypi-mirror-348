"""Generic plugin that copies and transforms messages between operational pictures"""

from c2sketch.execute.plugins import Agent
from c2sketch.models import *

class TransferAgent(Agent):

    title = "Data Transfer"
    description = "Generic plugin that copies and transforms messages between operational pictures"
    def interact(self, time: int, models: ModelSet) -> list[ScenarioEvent]:
        
        # field_names = config.get('field_names')
        # field_names = [name.strip() for name in field_names.split(';')] if field_names is not None else []

        # field_values = config.get('field_values')
        # field_values = [name.strip() for name in field_values.split(';')] if field_values is not None else []

        # fields = list(zip(field_names,field_values))

        # input_picture = config.get('source_op')
        # input_picture = sorted(pictures.keys())[0] if input_picture is None else input_picture
        
        # input_replacements = {'i-'+key:value for key,value in input.items()} if input is not None else dict()

        # def process(messages):
        #     transfers = list()
        #     for message in messages:
        #         replacements = {**{'m-' + key: value for key,value in message.items()},**input_replacements}
        #         transfer = dict()
        #         for key, value in fields:
        #             try:
        #                 transfer[key] = value.format(**replacements)
        #             except KeyError:
        #                 pass
        #         transfers.append(transfer)
        
        return super().interact(time, models)
    
def config_type():
    return RecordType(None,'data_transfer_config',[
        RecordTypeField('source','string'),# Which IFS should be watched for new messages, can be left blank if there is only one.
        RecordTypeField('source','string'),# Which IFS should be watched for new messages, can be left blank if there is only one.
        RecordTypeField('field_names','string'), #Which fields to create in the output message
        RecordTypeField('field_values','string'), #A specification of the fields to copy from
        RecordTypeField('update_interval','string'), #Interval (in seconds) at which the information is transferred.
    ])