from toppyt import (DataSource, Editor, all_tasks,
                    enter_information, forever, view_information, write_information)
from toppyt.bulma import BulmaButton
from toppyt.patterns import after_action
from c2sketch.app.plugins import InformationSpaceUI
from c2sketch.app.ui import record_editor


class MessageTable(Editor):
    def __init__(self, fields):
        self.fields = fields

    def generate_ui(self,name='v'):
        messages = self._raw if isinstance(self._raw,list) else list()
        rows = ''.join([self.row_html(message, name) for message in messages])
        header = ''
        
        row = ''.join([f'<th>{field.name}</th>' for field in self.fields])
        header = f'<tr>{row}<th></th></tr>' #Extra column for actions
        return f'<div class="field"><table class="table is-fullwidth is-striped">{header}{rows}</table></div>'
    
    def row_html(self, message, name):
        columns_html = list()
        for field in self.fields:
            if field.name in message and message[field.name] is not None:
                if field.type == 'real':
                    value = message[field.name]
                    columns_html.append(self.column_html('-' if value is None else f'{value:.3f}'))
                elif field.type == 'real2':
                    value = message[field.name]
                    columns_html.append(self.column_html('-' if value is None else f'{value[0]:.3f} {value[1]:.3f}'))
                elif field.type == 'real3':
                    value = message[field.name]
                    columns_html.append(self.column_html('-' if value is None else f'{value[0]:.3f} {value[1]:.3f} {value[2]:.3f}'))
                else:
                    columns_html.append(self.column_html(message[field.name]))
            else:
                columns_html.append(self.column_html('-'))
                
        related_tasks = message.get('RELATED_TASKS',list())
        if related_tasks:
            buttons = list()
            for task_name, value in related_tasks:
                buttons.append(f'<button class="button" onclick="toppyt_notify(this,true,\'{name}\',\'{value}\');return false;">{task_name}</a>')
            columns_html.append(f'<td>{"".join(buttons)}</td>')

        else:
            columns_html.append(self.column_html(''))

        return f'<tr>{"".join(columns_html)}</tr>'

    @staticmethod
    def column_html(col):
        return f'<td>{col}</td>'

def control_ui(rsource: DataSource | None, wsource: DataSource | None, op_type = None, plugin_config = None):
    tasks = []

    if rsource is not None:
        fields = [] if op_type is None else op_type.fields
        tasks.append(view_information(rsource,editor= MessageTable(fields)))

    if wsource is not None and op_type is not None:
        tasks.append(forever(after_action(
            enter_information(editor=record_editor(op_type)),
            BulmaButton('Send',icon='envelope'),
            lambda message: write_information(wsource,lambda ws:ws.write(message))
        )))
    
    return all_tasks(*tasks)

#Define plugin
data_table = InformationSpaceUI (
    title = 'Data table',
    description = 'Generic tabular display of a list of messages',
    config_type = None,
    control_ui = control_ui
)