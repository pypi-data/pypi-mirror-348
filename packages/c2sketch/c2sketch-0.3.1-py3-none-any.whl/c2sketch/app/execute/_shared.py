from toppyt import (ParallelTask, ViewEditor, view_information, update_information, enter_information,
                    write_information, forever, after_value)
from toppyt.bulma import BulmaRecordEditor, BulmaButtons, BulmaButtonSpec
from c2sketch.app.ui import BulmaToggleField
from c2sketch.models import ScenarioID
from c2sketch.app.data import ExecutionStore

def view_execution_time(execute_store: ExecutionStore, execution_id: ScenarioID):
    editor = ViewEditor(lambda time: f'<span class="time-display">T = {time}</span>')
    return view_information(execute_store,lambda es:es.execution_time(execution_id),editor=editor)

def control_execution_timer(execute_store: ExecutionStore, execution_id: ScenarioID):

    def edit_options():
        editor = BulmaRecordEditor([
            ("playback",BulmaToggleField(text="Playback",sync=True)),
            ("record",BulmaToggleField(text="Record",sync=True))
        ])
        
        return update_information(execute_store,
                                    lambda es:es.execution_options(execution_id),
                                    lambda es, o:es.set_execution_options(execution_id,o),
                                    editor=editor)
    def timer_actions():
        actions = [
            BulmaButtonSpec('reset','Reset','clock-rotate-left',is_compact=True),
            BulmaButtonSpec('step-forward','Step forward','step-forward',is_compact=True),
            BulmaButtonSpec('play','Play','play',is_compact=True),
            BulmaButtonSpec('stop','Stop','stop',is_compact=True)
        ]

        def do_action(action):
            match action:
                case 'reset':
                    return write_information(execute_store,lambda es: es.reset_execution(execution_id))
                case 'step-forward':
                    return write_information(execute_store,lambda es: es.step_timer(execution_id))
                case 'play':
                    return write_information(execute_store,lambda es: es.start_timer(execution_id))
                case 'stop':
                    return write_information(execute_store,lambda es: es.stop_timer(execution_id))
        return forever(
            after_value(enter_information(editor=BulmaButtons(actions,has_addons=True)),do_action)
        )
    
    def layout(parts, task_tag):
        return f'''
        <div {task_tag} class="timer-control">
        {parts['options']}
        {parts['actions']}
        </div>
        '''
    return ParallelTask([
        ('options',edit_options()),
        ('actions',timer_actions())
    ],layout=layout)