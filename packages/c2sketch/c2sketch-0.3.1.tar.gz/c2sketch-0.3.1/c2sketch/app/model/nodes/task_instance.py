
from c2sketch.models import *
from ...data import ModelStore
from ...patterns import choose_task, view_with_edit
from ...ui import view_title, record_editor, map_ui, after_dialog, TableChoice, TableSelect, SourceView, SourceEditor
from toppyt import view_information, enter_information, update_information, all_tasks, after_task
from toppyt import read_information, write_information, with_information, ParallelTask, TaskVariable, TaskStatus, TaskResult
from toppyt import constant, any_task, forever, map_value, after_value, MappedEditor
from toppyt.patterns import continuous_choice, edit_in_dialog
from toppyt.bulma import BulmaRecordEditor, BulmaTextInput, BulmaTextArea, BulmaButtons, BulmaSelect, BulmaTable, BulmaButtonSpec
from typing import Any

__all__ = ('edit_task_instance_node',)

def edit_task_instance_node(model_store: ModelStore, model_id, task_id, path_var):
    #Edit parameters
    #Edit info space bindings
    def choose(general):
        if general is None:
            return view_information(f'Task instance "{task_id}" does not exist.')
        
        def layout(parts,task_tag):
            return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
        
        return ParallelTask ([
            ('title',view_title(general['name'])),
            ('main',choose_task([
            ('Attributes','file-alt', edit_instance_attributes(model_store, model_id, task_id)),
            ('Parameter','table-cells', edit_instance_parameter(model_store, model_id, task_id)),
            ('Information Requirements','circle-info', edit_info_bindings(model_store, model_id, task_id)),
            ('Constraints','ban',edit_task_instance_contraints(model_store, model_id, task_id)),
            ('Source','code', edit_task_instance_source(model_store,model_id,task_id,path_var)),
            ],'Attributes'))
        ],layout=layout)
    return with_information(model_store,lambda ps:ps.task_instance_attributes(model_id, task_id),choose,refresh=False)


def edit_instance_attributes(model_store: ModelStore, model_id: ModelID, task_id: TaskID):
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled= True)),
            ('title',BulmaTextInput(label = 'Title', disabled = True)),
            ('description',BulmaTextArea(label= 'Description', disabled = True))
        ])
        return view_information(model_store,lambda ms:ms.task_instance_attributes(model_id, task_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title')),
            ('description',BulmaTextArea(label = 'Description'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ms:ms.write_task_instance_attributes(model_id,task_id,updated_fields))

    return view_with_edit(view(),edit,save)
   
def edit_instance_parameter(model_store: ModelStore, model_id, task_id):

    def view(parameter_type):
        editor = record_editor(parameter_type,disabled=True)          
        return view_information(model_store, lambda ps:ps.task_instance_parameter(model_id, task_id), editor=editor)
    
    def edit(parameter_type, fields):
        editor = record_editor(parameter_type)         
        return update_information(fields, editor=editor)

    def save(updated_fields):
        return write_information(model_store,lambda ps:ps.write_task_instance_parameter(model_id, task_id, updated_fields))

    def edit_with_type(parameter_type):
        if parameter_type is None:
            return constant(None)
        else:
            return view_with_edit(view(parameter_type),lambda value: edit(parameter_type,value),save)
        
    return with_information(model_store, lambda ps:ps.task_instance_parameter_type(model_id, task_id), edit_with_type, refresh=False)

def edit_info_bindings(model_store: ModelStore, model_id: ModelID, task_id: TaskID):
    
    def create_info_binding():
    
        def edit(value, errors):   
            name_editor = BulmaTextInput(label='Name', help = (errors['name'],'danger') if 'name' in errors else None)
            binding_editor = BulmaTextInput(label='Binding', help = (errors['binding'],'danger') if 'binding' in errors else None)
            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('binding',binding_editor)
            ])
            return update_information(value, editor=editor)
    
        def verify(value):
            if 'name' not in value or value['name'] is None or value['name'] == '':
                return constant({'name':'Name may not be empty'})
            return constant({})

        def save(value):
            name = value.get('name')
            type = None if 'type' not in value or value['type'] == '' else value['type']
            read = 'readwrite' in value and value['readwrite'] in ['read','readwrite']
            write = 'readwrite' in value and value['readwrite'] in ['write','readwrite']
            binding = None if 'binding' not in value or value['binding'] == '' else value['binding']
            return write_information(model_store, lambda ms: ms.task_instance_create_info_binding(model_id,task_id,name,type,read,write,binding))
  
        return edit_in_dialog('Add Information requirement',constant({}),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def update_info_binding(req_name:str):
        def load():
            async def read(ms: ModelStore):
                req = await ms.task_instance_get_info_binding(model_id,task_id,req_name)
                value = {'name': req_name}
                if req.binding is not None:
                    value['binding'] = req.binding
                return value 
            return read_information(model_store, read)
               
        def edit(value, errors):
            name_editor = BulmaTextInput(label='Name',disabled=True)
            binding_editor = BulmaTextInput(label='Binding', help = (errors['binding'],'danger') if 'binding' in errors else None)
            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('binding',binding_editor)
            ])
            return update_information(value, editor=editor)
        
        def verify(value):
            return constant({})
        
        def save(value):
            name = value.get('name')
            binding = None if 'binding' not in value or value['binding'] == '' else value['binding']
            return write_information(model_store, lambda ms: ms.task_instance_update_info_binding(model_id,task_id,name,binding))
  
        return edit_in_dialog('Edit Information binding',load(),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])
    
    def delete_info_binding(req_name: str):
        return write_information(model_store, lambda ms: ms.task_instance_delete_info_binding(model_id,task_id,req_name))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add information binding','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.task_instance_info_space_bindings(model_id,task_id),
                choose_list_action_with_bindings)

        def choose_list_action_with_bindings(bindings: list[InformationSpaceBinding]):

            headers = ['Name','Binding']
            buttons = [BulmaButtonSpec('edit','Edit','edit',is_compact=True)
                      ,BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')
                      ]

            options = [(binding.name,
                        [binding.name,
                         '-' if binding.binding is None else binding.binding]
                         ,buttons) for binding in bindings]
            
            table_editor = BulmaTable(options,headers, with_select=False)
            return enter_information(editor=table_editor)
            
        def layout(parts, task_tag):
            return f'''
            <div {task_tag} style="margin: 10px">
            <div style="display: flex; flex-direction: row;">
                <div style="flex: 1; margin-right: 1em;"></div>
                <div style="flex: 0">{parts['global_actions']}</div>
            </div>
            <div>{parts['item_actions']}</div>
            </div>
            '''
        
        def result_builder(parts):
            if parts[0].value is not None: #Global action
                return TaskResult((parts[0].value,),TaskStatus.ACTIVE)
            if parts[1].value is not None: #Item actions
                return TaskResult((parts[1].value[0],parts[1].value[1]),TaskStatus.ACTIVE)
            return TaskResult(None,TaskStatus.ACTIVE)
        
        return ParallelTask([
            ('global_actions', choose_global_action()),
            ('item_actions', choose_list_action()),
        ], layout = layout, result_builder=result_builder)

    def handle_contact_action(action):
        match action:
            case ('create',):
                return create_info_binding()
            case ('edit',req_name):
                return update_info_binding(req_name)
            case ('delete',req_name):
                return delete_info_binding(req_name)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_contact_action
    )

def edit_task_instance_contraints(model_store: ModelStore, model_id, task_id):
    def view():
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor', disabled= True)),
            ('at_location',BulmaTextInput(label = 'At location', disabled = True))
        ])
        return view_information(model_store,lambda ms:ms.task_instance_constraints(model_id, task_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor')),
            ('at_location',BulmaTextInput(label = 'At location'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ms:ms.write_task_instance_constraints(model_id,task_id,updated_fields))

    return view_with_edit(view(),edit,save)

def edit_task_instance_source(model_store: ModelStore, model_id: ModelID, task_id: TaskID, path_var: TaskVariable[str]):
    
    def view():
        return view_information(model_store,lambda ms: ms.task_instance_source(model_id,task_id),editor=SourceView())
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return after_task(write_information(model_store,lambda ms: ms.write_task_instance_source(model_id,task_id,value)),
            lambda node_id: constant(None)
            if node_id == task_id else (write_information(path_var,lambda pv:pv.write(task_node_path(model_id,node_id))))
        )
    
    def task_node_path(model_id, node_id):
        return f'/model/{model_id}' if node_id is None else f'/model/{model_id}/ti/{node_id}'
    
    return view_with_edit(view(),edit,save)