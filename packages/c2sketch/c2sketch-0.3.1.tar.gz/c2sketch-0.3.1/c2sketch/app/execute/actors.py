"""Support for role-playing actors during execution"""

from toppyt import (ParallelTask, TaskVariable,
                    all_tasks, constant,
                    forever,
                    update_information,
                    with_information, write_information)
from functools import partial
from c2sketch.models import *
from ..config import AppConfig
from ..plugins import AppPluginLoader
from ..ui import *
from ..patterns import action_choice
from ..data import ModelStore, ExecutionStore
from ._shared import control_execution_timer, view_execution_time

__all__ = ['execute_scenario']

class MessageTable(Editor):

    def start(self, value: list[Record] | None) -> None:
        self.value = value if value is not None else []

    def generate_ui(self,name='v', task_tag = ''):

        header_fields = []
        for message in self.value:
            for field in message.fields.keys():
                if field not in header_fields:
                    header_fields.append(field)
    
        row = ''.join([f'<th>{field}</th>' for field in ['SEQ','TIME'] + header_fields])
        header = f'<tr>{row}<th></th></tr>' #Extra column for actions
        rows = ''.join([self.row_html(header_fields, message, name) for message in self.value])
        return f'<div {task_tag} class="field"><table class="table is-fullwidth is-striped">{header}{rows}</table></div>'
    
    def row_html(self, fields, message: Record, name):
        columns_html = [self.column_html(message.sequence_number),self.column_html(message.create_time)]
        for field in fields:
            if field in message.fields and message.fields[field] is not None:
                columns_html.append(self.column_html(message.fields[field]))
            else:
                columns_html.append(self.column_html('-'))
                
        return f'<tr>{"".join(columns_html)}</tr>'

    @staticmethod
    def column_html(col):
        return f'<td>{col}</td>'

def execute_scenario(config: AppConfig, model_store: ModelStore, execute_store: ExecutionStore, plugins: AppPluginLoader, scenario_id: ScenarioID, actor_id: ActorID, path_var, cookie_jar):
    
    group_selection: TaskVariable[ActorID|None] = TaskVariable(None)
    task_selection: TaskVariable[list[TaskID] | TaskID] = TaskVariable([])
    
    def select_group():

        def to_nodes(actor_ids):
            group_nodes = [{'name':local_id_from_global_id(actor_id)[0],'icon':'users','value':actor_id,'children':[]} for actor_id in sorted(actor_ids)]
            root_node = [{'name':'All groups','icon':'folder','value':None,'children':group_nodes}]
            return root_node
        return with_information(execute_store, lambda es:es.actor_groups(scenario_id,actor_id),
            lambda groups: update_information(group_selection,editor=TreeChoice(to_nodes(groups)))
        )
    
    def select_tasks():
        def to_nodes(task_ids,task_def_ids):
            grouped = {}
            for task_id, is_definition in [(t,False) for t in sorted(task_ids)] + [(t,True) for t in sorted(task_def_ids)] :
                local_id, model_id = local_id_from_global_id(task_id)
             
                if not model_id in grouped:
                    grouped[model_id] = {'name': model_id, 'icon':'sitemap','value': None, 'children': []}
                
                node = grouped[model_id]
                segments = local_id.split('.')
                for segment in segments[:-1]:
                    if not node['children'] or node['children'][-1]['name'] != segment:
                        node['children'].append({'name': segment,'icon':'check','value': None, 'children':[]})
                    node = node['children'][-1]
                
                if is_definition:
                    node['children'].append({'name': segments[-1],'icon': 'plus','value': f'd:{task_id}','children':[]})
                else:
                    node['children'].append({'name': segments[-1],'icon': 'check','value': f't:{task_id}','children':[]})

            #Merge all groups
            task_nodes = [node for model_id in sorted(grouped.keys()) for node in grouped[model_id]['children']]
            root_node = [{'name':'All tasks','icon':'folder','value':None,'children':task_nodes}]
           
            return root_node
        
        #TEMP: Only select one task to filter on
        async def read_one(sel: TaskVariable[list[TaskID]]):
            value = await sel.read()
            if isinstance(value,list) and value:
                return f't:{value[0]}'
            if isinstance(value,str):
                return f'd:{value}'
            return None
            
        async def write_one(sel: TaskVariable[list[TaskID]], update: TaskID | None):
            if update is None or update == '':
                value = []
            elif update.startswith('t:'):
                value = [update[2:]]
            elif update.startswith('d:'):
                value =  update[2:]
            return await sel.write(value)
            
        return with_information(execute_store, lambda es:es.actor_concrete_atomic_tasks(scenario_id,actor_id),
            lambda tasks: with_information(execute_store, lambda es:es.actor_concrete_task_definitions(scenario_id,actor_id),
                lambda task_defs:
                    update_information(task_selection,read_one,write_one,editor=TreeChoice(to_nodes(tasks,task_defs)))
        ))
       
    def select_action():
        actions = [
                ('add','Change location...','map-pin',change_location(execute_store,scenario_id,actor_id)),
                ('join_group','Join group...','user-plus',join_group(execute_store,scenario_id,actor_id)),
                ('leave_group','Leave group...','user-minus',leave_group(execute_store,scenario_id,actor_id))
                ]
        return forever(action_choice(actions))
    
    def main(is_active):
        if is_active:
            def layout(parts, task_tag):
                return f'''
                <div {task_tag} class="prepare-grid">
                    <div class="prepare-header">{execute_header(parts['actor_title'],parts['actor_locations'], parts['execution_time'], parts['execution_timer_control'],parts['app_mode'])}</div>
                    <div class="prepare-body">
                        <div class="prepare-side">
                            <div class="panel-block buttons">
                            {parts['actor_actions']}
                            </div>
                            <div class="panel-block">
                            {parts['choose_group']}
                            {parts['choose_tasks']}
                            </div>
                        </div>
                        <flex-resizer></flex-resizer>
                        <div class="prepare-main">
                        <div class="container prepare-inner">
                        {parts['work_tasks']}
                        </div>
                        </div>
                    </div>
                </div>
                '''
            return ParallelTask(
                [('actor_title',switch_execution_actor(execute_store, scenario_id, actor_id, path_var))
                ,('actor_locations',view_execution_actor_locations(execute_store, scenario_id, actor_id))
                ,('execution_time',view_execution_time(execute_store, scenario_id))
                ,('execution_timer_control',control_execution_timer(execute_store, scenario_id))
                ,('actor_actions',select_action())
                ,('choose_group',select_group())
                ,('choose_tasks',select_tasks())
                ,('work_tasks',work_on_tasks(execute_store, plugins, scenario_id, actor_id, task_selection, group_selection))
                ,('app_mode',choose_app_mode(path_var))
                ],layout=layout,result_builder=lambda rs:rs[-1])
        else:
            def layout(parts, task_tag):
                return f'''
                <div {task_tag} class="prepare-grid">
                    <div class="prepare-header">{model_header(config.name, '','', '',parts['app_mode'])}</div>
                    <div class="prepare-body">
                        <div class="container">
                        {parts['message']}
                        </div>
                    </div>
                </div>
                '''
            return ParallelTask(
            [('message',view_information(f'Scenario {scenario_id} is not currently active'))
            ,('app_mode',choose_app_mode(path_var))
            ],layout=layout,result_builder=lambda rs:rs[-1])
            
    return with_information(execute_store,lambda es: es.execution_exists(scenario_id),main)                      

def switch_execution_actor(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID, path_var):
   
    def switch(actors):
        options = [(label,f'/execute/{scenario_id}/actor/{id}') for (id,label) in actors]
        editor = BulmaSelect(options=options,allow_empty=False,sync=True)
    
        return update_information(path_var,editor=editor)
    
    return with_information(execute_store,lambda es: es.list_actors(scenario_id),switch)

def view_execution_actor_locations(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID):
    editor = BulmaTextView()
    return view_information(execute_store, lambda es: es.actor_locations(scenario_id,actor_id),editor=editor)

def change_location(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID):
    
    def enter(task, validate):
        def change_location(location_ids):
            editor = BulmaSelect(options=[(label,value) for value, label in location_ids],label='Location')
            return update_information(task, editor=editor)
        return with_information(execute_store,lambda es: es.list_locations(scenario_id),change_location)
        
    def validate(task, action):
        return constant({})
    def save(task):
        if task is None:
            return constant(None)
        
        return write_information(execute_store,lambda es:es.emit_move_event(scenario_id,actor_id,task))

    return after_dialog('Change location...',
                enter,
                validate,
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('save','Save','save',save)
                ])

def join_group(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID):
     
    def enter(task, validate):
        def select_group(location_ids):
            editor = BulmaSelect(options=[(label,value) for value, label in location_ids],label='Group')
            return update_information(task, editor=editor)
        #TODO: list only affiliation options (filtered to prevent cycles)
        return with_information(execute_store,lambda es: es.list_actors(scenario_id),select_group)
        
    def validate(task, action):
        return constant({})
    def save(task):
        if task is None:
            return constant(None)
        
        return write_information(execute_store,lambda es:es.emit_join_group_event(scenario_id,actor_id,task))

    return after_dialog('Join group...',
                enter,
                validate,
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('save','Join','save',save)
                ])

def leave_group(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID):
     
    def enter(task, validate):
        def select_group(location_ids):
            editor = BulmaSelect(options=[(value,value) for value in location_ids],label='Group')
            return update_information(task, editor=editor)

        return with_information(execute_store,lambda es: es.actor_groups(scenario_id,actor_id),select_group)
          
    def validate(task, action):
        return constant({})
    def save(task):
        if task is None:
            return constant(None)
        
        return write_information(execute_store,lambda es:es.emit_leave_group_event(scenario_id,actor_id,task))

    return after_dialog('Leave group...',
                enter,
                validate,
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('save','Leave','save',save)
                ])

def select_tasks(execute_store: ExecutionStore, scenario_id: ScenarioID, actor_id: ActorID, selection: TaskVariable[list[TaskID]]):
    
    def update_selection(atomic_concrete_tasks):
        editor = CheckboxChoice(options=atomic_concrete_tasks,label='Concrete tasks')
        return update_information(selection, editor=editor)
            
    return with_information(execute_store, lambda es: es.actor_concrete_atomic_tasks(scenario_id,actor_id),
                            update_selection)

def work_on_tasks(execute_store: ExecutionStore, plugins: AppPluginLoader, scenario_id: ScenarioID, actor_id: ActorID, task_selection: TaskVariable[list[TaskID]|TaskID], group_selection: TaskVariable[TaskID|None]):
  
    def interact_with_info_spaces_for_locations(ifs_ids, task_ids):
        def view_relevant(relevant_ifs_ids):
            return all_tasks(*(interact_with_info_space(ifs_id) for ifs_id in relevant_ifs_ids))
        
        if task_ids:
            return with_information(execute_store,lambda es: es.task_information_spaces(scenario_id,task_ids[0]),view_relevant)
        else:
            return view_relevant(ifs_ids)
     
    def interact_with_info_space(ifs_id):
        
        def view_info_space_title():
            return view_information(ifs_id,editor=ViewEditor(lambda id: f'<div class="content"><h2>{local_id_from_global_id(id)[0]}</h2></div>'))
        def view_info_space_content():
            def view(mb_plugin):
                if mb_plugin is None:
                    editor = MessageTable()
                else:
                    plugin_cls = plugins.info_space_graphics[mb_plugin]
                    plugin = plugin_cls()
                    models = execute_store.executions[scenario_id].models #FIXME: No direct access
                    time = execute_store.executions[scenario_id].time
                    plugin.start(time,ifs_id,models)

                    editor = ViewEditor(lambda records: plugin.render_svg(time,records))

                return view_information(execute_store, lambda es: es.info_space_content(scenario_id,ifs_id),editor=editor)

            return with_information(execute_store,lambda es:es.info_space_graphic_plugin(scenario_id,ifs_id),view)

        def send_information():
            def enter(type, record, validate):
                if type is None:
                    editor = MappedEditor(
                        BulmaTextArea(label='data'),
                        lambda fields: None if fields is None else fields.get('data'),
                        lambda data: None if data is None else {'data':data}
                        )
                else:
                    editor = record_editor(type)
                return update_information(record, editor=editor)
                 
            def validate(type, fields, action):
                return constant({})
            
            def save(fields: Record | None):
                if fields is None:
                    return constant(None)
                
                return write_information(execute_store,lambda es:es.emit_information_event(scenario_id,actor_id,ifs_id,fields))

            return with_information(
                execute_store,
                lambda es: es.info_space_type(scenario_id,ifs_id),
                lambda type: after_dialog('Send information...',
                        partial(enter,type),
                        partial(validate,type),
                        [('cancel','Cancel','ban',lambda _: constant(None))
                        ,('send','Send','envelope',save)
                        ]))
    

        return all_tasks(
            view_info_space_title(),
            forever(action_choice([('send','Send...','envelope',send_information())],compact_buttons=False)),
            view_info_space_content()
        )
            
    def initiate_task_instance(task_id):
       

        def enter(parameter_type, parameter,validate):
            editor = record_editor(parameter_type)
            return update_information(parameter,editor=editor)
        
        def validate(parameter, action):
            return constant({})
        
        def save(parameter):
            if parameter is None:
                return constant(None)
            
            return write_information(execute_store,lambda es:es.emit_task_initiate_event(scenario_id,actor_id,task_id,parameter))

        return with_information(execute_store, lambda es: es.task_definition_parameter_type(scenario_id, task_id),
            lambda parameter_type: forever(
                inline_dialog(
                    partial(enter,parameter_type),
                    validate,
                    [('save','Initiate','plus',save)]) 
            ))
        
    def work(task_ids_or_def):
        if isinstance(task_ids_or_def,TaskID):
            return initiate_task_instance(task_ids_or_def)  
        if isinstance(task_ids_or_def,list):
            return with_information(execute_store,lambda es: es.actor_location_information_spaces(scenario_id, actor_id)
                        ,lambda ifs_ids: interact_with_info_spaces_for_locations(ifs_ids,task_ids_or_def))
    return with_information(task_selection,lambda ts: ts.read(),work)
    