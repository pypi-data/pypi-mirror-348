"""Creating and managing execution runs"""

from toppyt import (ParallelTask, TaskResult, TaskStatus, TaskVariable,
                    after_value, all_tasks, any_task, constant,
                    enter_information, forever,
                    update_information,
                    with_information,
                    with_dependent,
                    write_information,
                    read_information)
from toppyt.bulma import BulmaButtons, BulmaButtons, BulmaButtonSpec, BulmaTable, BulmaPagination, BulmaHidden
from toppyt.patterns import continuous_choice, edit_in_dialog, view_in_dialog

from c2sketch.models import *
from ..config import AppConfig
from ..data import ModelStore, ExecutionStore
from ..ui import *
from ..patterns import action_choice, choose_task
from ...visualizations import  svg_task_hierarchy
from ._shared import control_execution_timer, view_execution_time

from functools import partial
from math import ceil
from typing import TypeVar

__all__ = ['manage_executions']

def manage_executions(config: AppConfig, model_store: ModelStore, execute_store: ExecutionStore, path_var, cookie_jar):
    
    selection = TaskVariable(None)
 
    def select_execution():
        def to_nodes(executions,scenarios):
            execution_nodes = [
                {'name': execution_id,'icon': 'play','value': f'e:{execution_id}','children':[]}
                for execution_id in sorted(executions)
            ]
            
            scenario_nodes = [
                {'name': scenario_id,'icon': 'file','value': f's:{scenario_id}','children':[]}
                for scenario_id in sorted(scenarios)
            ]
            nodes = [{'name': 'Active scenario\'s','icon':'folder','value':None,'children': execution_nodes},
                     {'name': 'Saved scenario\'s','icon':'folder','value':None,'children': scenario_nodes}
                     ]
            return nodes

        return with_information(execute_store, lambda es:es.list_executions(),
            lambda executions: 
                with_information(execute_store, lambda es:es.list_scenarios(),
                lambda scenarios:              
                    update_information(selection, editor=TreeChoice(to_nodes(executions,scenarios)))
                )
        )
    def select_action(selection):
        execution_id = None if selection is None or not selection.startswith('e:') else selection[2:]
        scenario_id = None if selection is None or not selection.startswith('s:') else selection[2:]
        actions = [
                ('new','New...','plus',add_new_execution(model_store,execute_store)),
                ('load','Load...','folder-open',None if scenario_id is None else load_execution(model_store,execute_store,scenario_id)),
                ('save','Save...','save',None if execution_id is None else save_execution(execute_store,execution_id)),
                ('delete','Delete...','trash',None if execution_id is None else delete_execution(execute_store,execution_id))
                ]
        return forever(action_choice(actions))

    def manage_selected_execution():    
        return with_information(selection,lambda s:s.read(),lambda selection_id:
                view_information('')
                if selection_id is None or not selection_id.startswith('e:') else
                with_information(execute_store,lambda es: es.execution_exists(selection_id[2:]),lambda exists:
                    view_information('')
                    if not exists else
                    manage_running_execution(execute_store,path_var,selection_id[2:])
                ))
    def control_selected_execution_timer():    
        return with_information(selection,lambda s:s.read(),lambda selection_id:
                view_information('')
                if selection_id is None or not selection_id.startswith('e:') else
                with_information(execute_store,lambda es: es.execution_exists(selection_id[2:]),lambda exists:
                    view_information('')
                    if not exists else
                    control_execution_timer(execute_store,selection_id[2:])
                ))

    def view_selected_execution_time():
        return with_information(selection,lambda s:s.read(),lambda selection_id:
                view_information('')
                if selection_id is None or not selection_id.startswith('e:') else
                with_information(execute_store,lambda es: es.execution_exists(selection_id[2:]),lambda exists:
                    view_information('')
                    if not exists else
                    view_execution_time(execute_store,selection_id[2:])
                ))

    def layout(parts, task_tag):
        return f'''
        <div {task_tag} class="execute-grid">
            <div class="execute-header">{execute_header('','',parts['view_time'],parts['control_execution'],parts['app_mode'])}</div>
            <div class="execute-body">
                <div class="execute-side">
                    <div class="panel-block buttons">
                    {parts['execution_actions']}
                    </div>
                    <div class="panel-block">
                    {parts['choose_execution']}
                    </div>
                </div>
                <flex-resizer></flex-resizer>
                <div class="execute-main">
                <div class="container execute-inner">
                {parts['preview_execution']}
                </div>
                </div>
            </div>
        </div>
        '''

    return ParallelTask(
        [('choose_execution',select_execution())
        ,('execution_actions',with_information(selection,lambda s:s.read(), select_action))
        ,('preview_execution',manage_selected_execution())
        ,('view_time',view_selected_execution_time())
        ,('control_execution',control_selected_execution_timer())
        ,('app_mode',choose_app_mode(path_var))
        ],layout=layout,result_builder=lambda rs:rs[-1])

def manage_running_execution(execute_store: ExecutionStore, path_var: TaskVariable[str], execution_id: ScenarioID):

    def view_task_decompostion():
        def view(model_id: ModelID, model_set: ModelSet):
            return view_information(svg_task_hierarchy(model_set, model_id),editor=SVGCanvas())
    
        return with_information(execute_store,lambda es: es.execution_model(execution_id),lambda r: view(*r))
       
    return choose_task([
        ('Actors','user',manage_actor_status(execute_store, execution_id, path_var)),
        ('Events','calendar',edit_events(execute_store, execution_id)),
        ('Task decomposition','sitemap',view_task_decompostion())
    ],'Actors')

def manage_actor_status(execute_store: ExecutionStore, execution_id: ScenarioID, path_var: TaskVariable[str]):
    page = TaskVariable(1)
    selection = TaskVariable(set())
    limit = 10

    def handle_event_action(action):
        match action:
            case ('start_all',):
                return write_information(execute_store,lambda es: es.start_all_agents(execution_id))
            case ('stop_all',):
                return write_information(execute_store,lambda es: es.stop_all_agents(execution_id))
            case ('view',actor_id):
                return write_information(path_var,lambda pv: pv.write(f'/execute/{execution_id}/actor/{actor_id}'))
            case ('start',actor_id):
                return write_information(execute_store,lambda es:es.start_agent(execution_id,actor_id))
            case ('stop',actor_id):
                return write_information(execute_store,lambda es:es.stop_agent(execution_id,actor_id))
            case ('start_selection',actor_ids):
                return write_information(execute_store,lambda es:es.start_agents(execution_id,actor_ids))
            case ('stop_selection',actor_ids):
                return write_information(execute_store,lambda es:es.stop_agents(execution_id,actor_ids))
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_actor_action_task(execute_store, execution_id,limit,page,selection),
        handle_event_action
    )

def select_actor_action_task(execute_store: ExecutionStore, execution_id: ScenarioID,
                         limit: int, page: TaskVariable[int],
                         selection: TaskVariable[set[ActorID]]):
    
    def choose_global_action():
        buttons = [BulmaButtonSpec('start_all','Start all agents','play'),
                   BulmaButtonSpec('stop_all','Stop all agents','stop')
                   ]
        return enter_information(editor=BulmaButtons(buttons,align='right'))

    def choose_list_action(page, selection_var: TaskVariable[set[ActorID]]):
        offset = (page - 1) * limit
        return with_information(execute_store,
                lambda es:es.list_actors(execution_id,limit,offset),
                lambda actors: with_information(execute_store,lambda es:es.agent_status(execution_id),
                lambda status: choose_list_action_with_actors(actors,status,selection_var)))
    
    def choose_list_action_with_actors(actors: list[tuple[ActorID,str]], status, selection_var: TaskVariable[set[ActorID]]):
        
        def enter_with_list(selection):
            headers = ['Actor','Active Agent']
            
            rows = []
            for (actor_id,actor_label) in actors:
                enabled_label = str(status[actor_id]) if actor_id in status else 'N/A'
                actions = [BulmaButtonSpec('view','View','eye',is_compact=True)]
                if actor_id in status:
                    actions = [BulmaButtonSpec('start','Start agent','play'),BulmaButtonSpec('stop','Stop agent','stop')] + actions
                rows.append((actor_id,[actor_label,enabled_label],actions,actor_id in selection))
            
            return enter_information(editor=BulmaTable(rows,headers))
        
        def update_selection(action):
            match(action):
                case ('select',item):
                    return select(selection_var,[item])
                case ('deselect',item):
                    return deselect(selection_var,[item])
                case ('select_all',):
                    return select(selection_var,[aid for aid,_ in actors])
                case ('deselect_all',):
                    return write_information(selection_var, lambda v: v.write(set()))
                    
            return constant(None)
        
        return with_dependent(with_information(selection_var, lambda v:v.read(),enter_with_list),update_selection)
        
    def choose_page(page_var):
        return with_information(execute_store,lambda ab:ab.num_actors(execution_id),lambda num: choose_page_with_num_actors(page_var,num))
    
    def choose_page_with_num_actors(page_var, num_actors: int):
        num_pages = ceil(num_actors / limit)
    
        return update_information(page_var, editor = BulmaPagination(num_pages))
    
    def choose_selection_action(selection_var):
        return with_information(selection_var, lambda v:v.read(), choose_with_selection)

    def choose_with_selection(selection):
        if len(selection) > 0:
            buttons = [BulmaButtonSpec('start_selection',f'Start selected agents','play'),
                       BulmaButtonSpec('stop_selection',f'Stop selected agents','stop')]
            return map_value(enter_information(editor=BulmaButtons(buttons)),lambda action: (action,list(selection)))
        else:
            return constant(None, stable = False)
    def layout(parts, task_tag):
        return f'''
        <div {task_tag} style="margin: 10px">
        <div style="display: flex; flex-direction: row;">
            <div style="flex: 1; margin-right: 1em;">{parts['selection_actions']}</div>
            <div style="flex: 0 0 content">{parts['global_actions']}</div>
        </div>
        <div>{parts['item_actions']}</div>
        <div style="margin-top: 5px">{parts['page']}</div>
        </div>
        '''
    
    def result_builder(parts):
        if parts[1].value is not None: #Global action
            return TaskResult((parts[1].value,),TaskStatus.ACTIVE)

        if parts[2].value is not None: #Item actions
            if parts[2].value[0] not in ['select','deselect','select_all','deselect_all']:
                return TaskResult((parts[2].value[0],parts[2].value[1]),TaskStatus.ACTIVE)
            
        if parts[3].value is not None: #Selection actions
            return TaskResult((parts[3].value[0],parts[3].value[1]),TaskStatus.ACTIVE)
  
        return TaskResult(None,TaskStatus.ACTIVE)
    
    return ParallelTask([
        ('page', choose_page(page)),
        ('global_actions', choose_global_action()),
        ('item_actions', ['page'], lambda page: choose_list_action(page.value, selection)),
        ('selection_actions',choose_selection_action(selection))
    ],layout=layout, result_builder=result_builder)

#Editing the event timeline

def event_type(event: ScenarioEvent) -> str:
    return {
        ScenarioInformationEvent: 'Send information',
        ScenarioTaskInitiateEvent: 'Initiate task',
        ScenarioJoinGroupEvent: 'Join group',
        ScenarioLeaveGroupEvent: 'Leave group',
        ScenarioEnterLocationEvent: 'Enter location',
        ScenarioLeaveLocationEvent: 'Leave location'
    }[event.__class__]

def event_time(event: ScenarioEvent) -> int:
    return event.time

def event_details(event: ScenarioEvent) -> str:
    match event:
        case ScenarioInformationEvent():
            return f'{event.fields} to {event.information_space} by {event.actor}'
        case ScenarioTaskInitiateEvent():
            return f'{event.task_definition}({event.parameter}) by {event.actor}'
        case ScenarioJoinGroupEvent():
            return f'{event.actor} joined {event.group}'
        case ScenarioLeaveGroupEvent():
            return f'{event.actor} left {event.group}'
        case ScenarioEnterLocationEvent():
            return f'{event.actor} entered {event.location}'
        case ScenarioLeaveLocationEvent():
            return f'{event.actor} left {event.location}'
    return '-'

def event_to_dict(event: ScenarioEvent) -> dict[str,Any]:
    match event:
        case ScenarioInformationEvent():
            return {'type':'Send information','time':event.time,'actor':event.actor,'information_space':event.information_space,'fields':event.fields}
        case ScenarioTaskInitiateEvent():
            return {'type':'Initiate task','time':event.time,'actor':event.actor,'task_definition':event.task_definition,'parameter':event.parameter,'trigger':event.trigger,'for_actor':event.for_actor}
        case ScenarioJoinGroupEvent():
            return {'type':'Join group','time':event.time,'actor':event.actor,'group':event.group}
        case ScenarioLeaveGroupEvent():
            return {'type':'Leave group','time':event.time,'actor':event.actor,'group':event.group}
        case ScenarioEnterLocationEvent():
            return {'type':'Enter location','actor':event.actor,'location':event.location}
        case ScenarioLeaveLocationEvent():
            return {'type':'Enter location','actor':event.actor,'location':event.location}
    return {}

def verify_event(value):
    errors = {}
    if 'type' not in value or value['type'] is None or value['type'] == '':
        errors['type'] = 'Type cannot be empty'
        return constant(errors)

    # Time and actor are always required
    if 'time' not in value or value['time'] is None or value['time'] == '':
        errors['time'] = 'Time cannot be empty'
    if 'actor' not in value or value['actor'] is None or value['actor'] == '':
        errors['actor'] = 'Actor cannot be empty'

    if value['type'] == 'Send information':
        if 'information_space' not in value or value['information_space'] is None or value['information_space'] == '':
            errors['information_space'] = 'Information space cannot be empty'
    
    if value['type'] == 'Initiate task':
        if 'task_definition' not in value or value['task_definition'] is None or value['task_definition'] == '':
            errors['task_definition'] = 'Task definition cannot be empty'

    if value['type'] == 'Join group' or value['type'] == 'Leave group':
        if 'group' not in value or value['group'] is None or value['group'] == '':
            errors['group'] = 'Group cannot be empty'
    if value['type'] == 'Enter location' or value['type'] == 'Leave location':
        if 'location' not in value or value['location'] is None or value['location'] == '':
            errors['location'] = 'Location cannot be empty'

    return constant(errors)

def event_from_dict(event_dict: dict[str,Any]) -> ScenarioEvent | None:
    if event_dict['type'] == 'Send information':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        information_space = event_dict.get('information_space')
        fields = event_dict.get('fields')
        for_actor = event_dict.get('for_actor')
        if time is not None and actor is not None and information_space is not None and fields is not None:
            return ScenarioInformationEvent(time,actor,information_space,fields,for_actor)
    if event_dict['type'] == 'Initiate task':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        task_definition = event_dict.get('task_definition')
        parameter = event_dict.get('parameter')
        trigger = event_dict.get('trigger')
        for_actor = event_dict.get('for_actor')
        if time is not None and actor is not None and task_definition is not None and parameter is not None:
            return ScenarioTaskInitiateEvent(time,actor,task_definition,parameter,trigger,for_actor)
    if event_dict['type'] == 'Join group':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        group = event_dict.get('group')
        if time is not None and actor is not None and group is not None:
            return ScenarioJoinGroupEvent(time, actor, group)
    if event_dict['type'] == 'Leave group':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        group = event_dict.get('group')
        if time is not None and actor is not None and group is not None:
            return ScenarioLeaveGroupEvent(time, actor, group)
    if event_dict['type'] == 'Enter location':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        location = event_dict.get('location')
        if time is not None and actor is not None and location is not None:
            return ScenarioEnterLocationEvent(time,actor,location)
    if event_dict['type'] == 'Leave location':
        time = event_dict.get('time')
        actor = event_dict.get('actor')
        location = event_dict.get('location')
        if time is not None and actor is not None and location is not None:
            return ScenarioLeaveLocationEvent(time,actor,location)
    return None

def edit_events(execute_store: ExecutionStore, execution_id: ScenarioID):
   
    page = TaskVariable(1)
    selection = TaskVariable(set())
    limit = 10

    def handle_event_action(action):
        match action:
            case ('create',):
                return create_event(execute_store, execution_id)
            case ('edit',event_id):
                return update_event(execute_store, execution_id, event_id)
            case ('delete',event_id):
                return delete_events(execute_store, execution_id, selection, [event_id])
            case ('delete_selection',event_ids):
                return delete_events(execute_store, execution_id, selection, event_ids)
            
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_event_task(execute_store, execution_id,limit,page,selection),
        handle_event_action
    )

def edit_event(execute_store: ExecutionStore, execution_id: ScenarioID, value, errors):
    def edit_type(type):
        help = (errors['type'],'danger') if 'type' in errors else None
        options = ['Send information','Initiate task','Join group','Leave group','Enter location','Leave location']
        return update_information(type, editor=BulmaSelect(options,label='Type',help=help,sync=True))
    
    def edit_details(type, details):
        details['type'] = type
        match type:
            case 'Send information':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        with_information(execute_store,lambda es:es.list_info_spaces(execution_id),lambda spaces:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('information_space',BulmaSelect(options=[(label,id) for (id,label) in spaces],label='Information space ID',help=(errors['information_space'],'danger') if 'information_space' in errors else None)),
                        ('fields',BulmaStrDictEditor(label='Fields'))
                ]))))
            case 'Initiate task':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        with_information(execute_store,lambda es:es.list_info_spaces(execution_id),lambda spaces:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('task_definition',BulmaTextInput(label='Task definition',help=(errors['task_definition'],'danger') if 'task_definition' in errors else None)),
                        ('parameter',BulmaStrDictEditor(label='Parameter')),
                        ('trigger',BulmaSelect(options=[(label,id) for (id,label) in spaces],label='Trigger'))
                ]))))
            case 'Join group':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('group',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Group ID',help=(errors['group'],'danger') if 'group' in errors else None))
                        ])))
            case 'Leave group':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('group',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Group ID',help=(errors['group'],'danger') if 'group' in errors else None))
                        ])))
            case 'Enter location':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        with_information(execute_store,lambda es:es.list_locations(execution_id),lambda locations:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('group',BulmaSelect(options=[(location,id) for (id,location) in locations],label='Location ID',help=(errors['location'],'danger') if 'location' in errors else None))
                        ]))))
            case 'Leave location':
                return with_information(execute_store,lambda es:es.list_actors(execution_id),lambda actors:
                        with_information(execute_store,lambda es:es.list_locations(execution_id),lambda locations:
                        update_information(details,editor = BulmaRecordEditor([
                        ('type',BulmaHidden()),
                        ('time',BulmaIntInput(label='Time',help=(errors['time'],'danger') if 'time' in errors else None)),
                        ('actor',BulmaSelect(options=[(label,id) for (id,label) in actors],label='Actor ID',help=(errors['actor'],'danger') if 'actor' in errors else None)),
                        ('group',BulmaSelect(options=[(location,id) for (id,location) in locations],label='Location ID',help=(errors['location'],'danger') if 'location' in errors else None))
                        ]))))      
        return constant({'type':type},False)
            
    return ParallelTask([
        ('type',[('type',value['type'])], lambda t: edit_type(t.value)),
        ('details',[('type',value['type']),('details',value)],lambda t,d: edit_details(t.value,d.value))
    ],result_builder = lambda results: results[-1])


def create_event(execute_store: ExecutionStore, execution_id: ScenarioID):
    def load():
        return constant({'type':'Send information'})
    
    def save(value):
        event = event_from_dict(value)
        if event is None:
            return constant(None)
        else:
            return write_information(execute_store,lambda es:es.insert_event(execution_id,event)) 

    return edit_in_dialog('Add event',load(),partial(edit_event,execute_store,execution_id),verify_event,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

def update_event(execute_store: ExecutionStore, execution_id: ScenarioID, event_id: int):
    def load(event_id):
        async def read(es: ExecutionStore):
            event = await es.get_event(execution_id, event_id)
            return event_to_dict(event)
        return read_information(execute_store,read)
    
    def save(value):
        event = event_from_dict(value)
        if event is None:
            return constant(None)
        else:
            return write_information(execute_store,lambda es:es.update_event(execution_id,event_id,event)) 

    return edit_in_dialog('Update event',load(event_id),partial(edit_event,execute_store,execution_id),verify_event,                
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('save','Save','save',is_enter=True,extra_cls='is-primary'),True,save)])
   
def delete_events(execute_store: ExecutionStore, execution_id: ScenarioID, selection_var: TaskVariable[set[int]], event_ids: list[int]):
    title = f'Delete event{"s" if len(event_ids) == 1 else ""}'

    def load():
        return None
    
    def view(_):
        names = ', '.join(map(str,event_ids))
        message = f'''
        The following event{"s" if len(event_ids) > 1 else ""} will be deleted: "{names}".
        This action cannot be undone.
        '''
        return view_information(message)

    def save(_):
        return all_tasks(
            deselect(selection_var, event_ids),
            write_information(execute_store, lambda es: es.delete_events(event_ids))
        )
    
    return view_in_dialog(title, load(), view, 
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False,lambda _ : constant(None))
            ,(BulmaButtonSpec('continue','Continue','arrow-right',is_enter=True,extra_cls='is-primary'),True,save)
            ])

T = TypeVar('T')
def select(var: TaskVariable[set[T]], items: Iterable[T]):
    async def update( var: TaskVariable[set[T]]):    
        await var.write((await var.read()).union(items))
    return write_information(var,update)

def deselect(var: TaskVariable[set[T]], items: Iterable[T]):
    async def update( var: TaskVariable[set[T]]):    
        await var.write((await var.read()).difference(items))
    return write_information(var,update)

def select_event_task(execute_store: ExecutionStore, execution_id: ScenarioID,
                         limit: int, page: TaskVariable[int],
                         selection: TaskVariable[set[int]]):
    
    def choose_global_action():
        buttons = [BulmaButtonSpec('create','Add event','plus')]
        return enter_information(editor=BulmaButtons(buttons,align='right'))

    def choose_list_action(page, selection_var: TaskVariable[set[int]]):
        offset = (page - 1) * limit
        return with_information(execute_store,
                lambda ab:ab.list_events(execution_id,limit,offset),
                lambda events: choose_list_action_with_events(events,selection_var))
    
    def choose_list_action_with_events(events: list[tuple[int,ScenarioEvent]], selection_var: TaskVariable[set[int]]):
        
        def enter_with_list(selection):
            headers = ['#','Time','Type','Details']
            buttons = [BulmaButtonSpec('edit','Edit','edit',is_compact=True)
                      ,BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')
                      ]

            options = [(eid,[eid,event_time(event),event_type(event),event_details(event)],buttons,eid in selection) for eid, event in events]
            table_editor = BulmaTable(options,headers)
            return enter_information(editor=table_editor)
        
        def update_selection(action):
            match(action):
                case ('select',item):
                    return select(selection_var,[int(item)])
                case ('deselect',item):
                    return deselect(selection_var,[int(item)])
                case ('select_all',):
                    return select(selection_var,[eid for eid,_ in events])
                case ('deselect_all',):
                    return write_information(selection_var, lambda v: v.write(set()))
                    
            return constant(None)
        
        return with_dependent(with_information(selection_var, lambda v:v.read(),enter_with_list),update_selection)
        
    def choose_page(page_var):
        return with_information(execute_store,lambda ab:ab.num_events(execution_id),lambda num: choose_page_with_num_events(page_var,num))
    
    def choose_page_with_num_events(page_var, num_events: int):
        num_pages = ceil(num_events / limit)
    
        return update_information(page_var, editor = BulmaPagination(num_pages))
    
    def choose_selection_action(selection_var):
        return with_information(selection_var, lambda v:v.read(), choose_with_selection)

    def choose_with_selection(selection):
        if len(selection) > 0:
            buttons = [BulmaButtonSpec('delete_selection',f'Delete selected {len(selection)} events','trash')]
            return map_value(enter_information(editor=BulmaButtons(buttons)),lambda action: (action,list(selection)))
        else:
            return constant(None, stable = False)
        
    def layout(parts, task_tag):
        return f'''
        <div {task_tag} style="margin: 10px">
        <div style="display: flex; flex-direction: row;">
            <div style="flex: 1; margin-right: 1em;">{parts['selection_actions']}</div>
            <div style="flex: 0">{parts['global_actions']}</div>
        </div>
        <div>{parts['item_actions']}</div>
        <div style="margin-top: 5px">{parts['page']}</div>
        </div>
        '''
    
    def result_builder(parts):
        if parts[1].value is not None: #Global action
            return TaskResult((parts[1].value,),TaskStatus.ACTIVE)

        if parts[2].value is not None: #Item actions
            if parts[2].value[0] not in ['select','deselect','select_all','deselect_all']:
                return TaskResult((parts[2].value[0],int(parts[2].value[1])),TaskStatus.ACTIVE)
            
        if parts[3].value is not None: #Selection actions
            return TaskResult((parts[3].value[0],parts[3].value[1]),TaskStatus.ACTIVE)
  
        return TaskResult(None,TaskStatus.ACTIVE)
    
    return ParallelTask([
        ('page', choose_page(page)),
        ('global_actions', choose_global_action()),
        ('item_actions', ['page'], lambda page: choose_list_action(page.value, selection)),
        ('selection_actions',choose_selection_action(selection))
    ],layout=layout, result_builder=result_builder)


def add_new_execution(model_store: ModelStore, execute_store: ExecutionStore):
    def enter(task, validate):

        def enter_name(name, validate):
            help = None
            if validate is not None and 'name' in validate:
                help = (validate['name'],'danger')
            
            return update_information(name,editor=BulmaTextInput(help=help,label='Scenario name'))
        
        def choose_model(model_ids, model_id):
            help = None
            if validate is not None and 'model_id' in validate:
                help = (validate['model_id'],'danger')
            options = [(label if label is not None else value,value) for (value,label,_) in model_ids]

            return update_information(model_id,editor=BulmaSelect(options=options,label='Model',help=help))
        
        def result(results):
            names = ['model_id','name']
            return TaskResult({k: r.value for k,r in zip(names,results)}, TaskStatus.ACTIVE)
    
        return with_information(model_store,lambda ps: ps.list_models(), lambda model_ids: ParallelTask([  
            ('model_id',choose_model(model_ids,None if task is None else task.get('model_id'))),
            ('name',enter_name(None if task is None else task.get('name'),validate))
        ],result_builder=result))
        
    def validate(task, action):
        if action == 'cancel':
            return constant({})
        
        def check_input(existing_scenarios):
            errors = {}

            name = None if task is None else task.get('name','')
           
            if 'model_id' not in task or task['model_id'] is None or task['model_id'] == '':
                errors['model_id'] = 'You need to select a model to start a scenario.'

            if not is_safe_name(name):
                errors['name'] = 'Name is not a valid name. It may not contain spaces and cannot start with a number.'
            else:
                if name in existing_scenarios:
                    errors['name'] = f'A scenario named \'{name}\' is already active.'

            return constant(errors)
        
        return with_information(execute_store, lambda es: es.list_executions(),check_input,refresh=False)
     
    def save(task):
        name = task.get('name','')
        if name == '':
            name = 'untitled'
        model_id = task.get('model_id')
        return write_information(execute_store,lambda ps:ps.create_execution(name,model_id))
    
    return after_dialog('New scenario...',
                enter,
                validate,
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('add','Add','plus',save)
                ])

def save_execution(execute_store: ExecutionStore, scenario_id: ScenarioID):
    def enter(name, validate):
        if name is None:
            name = scenario_id
        help = (validate['name'],'danger') if validate is not None and 'name' in validate else None
  
        return update_information(name,editor=BulmaTextInput(help=help,label='Scenario name'))

    def validate(name, action):
        if action == 'cancel':
            return constant({})
        
        def check_input(existing_scenarios):
            errors = {}

            if not is_safe_name(name):
                errors['name'] = 'Name is not a valid name. It may not contain spaces and cannot start with a number.'
            else:
                if name in existing_scenarios:
                    errors['name'] = f'A scenario named \'{name}\' already exists.'

            return constant(errors)
        
        return with_information(execute_store, lambda ms: ms.list_scenarios(),check_input,refresh=False)
     
    def save(name):
        return write_information(execute_store,lambda es:es.save_execution(scenario_id, name))

    return after_dialog('Save scenario...',
                enter,
                validate,
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('add','Add','plus',save)
                ])

def delete_execution(execute_store: ExecutionStore, scenario_id: ScenarioID):
    return write_information(execute_store, lambda es: es.delete_execution(scenario_id))

def load_execution(model_store: ModelStore, execute_store: ExecutionStore,scenario_id: ScenarioID):
    return write_information(execute_store, lambda es: es.load_execution(scenario_id))

