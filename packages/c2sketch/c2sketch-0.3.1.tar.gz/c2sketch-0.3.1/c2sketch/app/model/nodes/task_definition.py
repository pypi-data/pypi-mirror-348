__all__ = ('edit_task_def_node',)

from toppyt import ParallelTask, TaskVariable, TaskResult, TaskStatus, after_task, view_information, enter_information, update_information, read_information, all_tasks, with_information, write_information, constant
from toppyt.bulma import BulmaTextInput, BulmaTextArea, BulmaRecordEditor, BulmaSelect, BulmaButtonSpec, BulmaButtons, BulmaTable
from toppyt.patterns import continuous_choice, edit_in_dialog

from c2sketch.app.ui import SourceView, SourceEditor, view_title
from c2sketch.app.patterns import choose_task, view_with_edit
from c2sketch.app.data import ModelStore
from c2sketch.models import ModelID, TaskID, InformationSpaceRequirement, Trigger

def edit_task_def_node(model_store: ModelStore, model_id, task_id, path_var):
   
    def choose(general):
        if general is None:
            return view_information(f'Task definition "{task_id}" does not exist.')
        
        def layout(parts,task_tag):
            return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
        
        return ParallelTask ([
            ('title',view_title(general['name'])),
            ('main',choose_task([
            ('Attributes','file-alt', edit_task_def_attributes(model_store, model_id, task_id)),
            ('Information Requirements','circle-info', edit_info_reqs(model_store, model_id, task_id, path_var)),
            ('Triggers','bell', edit_task_def_triggers(model_store, model_id, task_id, path_var)),
            ('Constraints','ban',edit_task_def_contraints(model_store, model_id, task_id)),
            ('Source','code', view_task_def_source(model_store,model_id,task_id,path_var)),
            ],'Attributes'))
        ],layout=layout)
    
    return with_information(model_store,lambda ps:ps.task_def_attributes(model_id, task_id),choose,refresh=False)
    
def edit_task_def_attributes(model_store: ModelStore, model_id, task_id):
    
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('type',BulmaTextInput(label='Parameter type',disabled=True)),
            ('title',BulmaTextInput(label = 'Title', disabled = True)),
            ('description',BulmaTextArea(label= 'Description', disabled = True)) 
        ])
        return view_information(model_store,lambda ms: ms.task_def_attributes(model_id, task_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('type',BulmaTextInput(label='Parameter type')),
            ('title',BulmaTextInput(label = 'Title')),
            ('description',BulmaTextArea(label = 'Description'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ms:ms.write_task_def_attributes(model_id, task_id, updated_fields))

    return view_with_edit(view(),edit,save)

def edit_info_reqs(model_store: ModelStore, model_id: ModelID, task_id: TaskID, path_var: TaskVariable[str]):
    
    def create_info_req():
    
        def edit(value, errors):   
            name_editor = BulmaTextInput(label='Name', help = (errors['name'],'danger') if 'name' in errors else None)
            type_editor = BulmaTextInput(label='Type', help = (errors['type'],'danger') if 'type' in errors else None)
            rw_editor = BulmaSelect([('Read only','read'),('Write only','write'),('Read and Write','readwrite')],label='Read/write')
            binding_editor = BulmaTextInput(label='Binding', help = (errors['binding'],'danger') if 'binding' in errors else None)
            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('type',type_editor),
                ('readwrite',rw_editor),
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
            return write_information(model_store, lambda ms: ms.task_def_create_info_req(model_id,task_id,name,type,read,write,binding))
  
        return edit_in_dialog('Add Information requirement',constant({}),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def update_info_req(req_name:str):
        def load():
            async def read(ms: ModelStore):
                req = await ms.task_def_get_info_req(model_id,task_id,req_name)
                value = {'name': req_name}
                if req.type is not None:
                    value['type'] = req.type
                if req.read and req.write:
                    value['readwrite'] = 'readwrite'
                elif req.read:
                    value['readwrite'] = 'read'
                elif req.write:
                    value['readwrite'] = 'write'
                if req.binding is not None:
                    value['binding'] = req.binding
                return value 
            return read_information(model_store, read)
               
        def edit(value, errors):
            name_editor = BulmaTextInput(label='Name',disabled=True)
            type_editor = BulmaTextInput(label='Type', help = (errors['type'],'danger') if 'type' in errors else None)
            rw_editor = BulmaSelect([('Read only','read'),('Write only','write'),('Read and Write','readwrite')],label='Read/write')
            binding_editor = BulmaTextInput(label='Binding', help = (errors['binding'],'danger') if 'binding' in errors else None)
            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('type',type_editor),
                ('readwrite',rw_editor),
                ('binding',binding_editor)
            ])
            return update_information(value, editor=editor)
        
        def verify(value):
            return constant({})
        
        def save(value):
            name = value.get('name')
            type = None if 'type' not in value or value['type'] == '' else value['type']
            read = 'readwrite' in value and value['readwrite'] in ['read','readwrite']
            write = 'readwrite' in value and value['readwrite'] in ['write','readwrite']
            binding = None if 'binding' not in value or value['binding'] == '' else value['binding']
            return write_information(model_store, lambda ms: ms.task_def_update_info_req(model_id,task_id,name,type,read,write,binding))
  
        return edit_in_dialog('Edit Information requirement',load(),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])
    
    def delete_info_req(req_name: str):
        return write_information(model_store, lambda ms: ms.task_def_delete_info_req(model_id,task_id,req_name))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add information req','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.task_def_info_space_requirements(model_id,task_id),
                choose_list_action_with_reqs)

        def choose_list_action_with_reqs(reqs: list[InformationSpaceRequirement]):

            headers = ['Name','Type','Read','Write','Binding']
            buttons = [BulmaButtonSpec('edit','Edit','edit',is_compact=True)
                      ,BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')
                      ]

            options = [(req.name,
                        [req.name,
                         '-' if req.type is None else req.type,
                         'yes' if req.read else 'no',
                         'yes' if req.write else 'no',
                         '-' if req.binding is None else req.binding]
                         ,buttons) for req in reqs]
            
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
                return create_info_req()
            case ('edit',req_name):
                return update_info_req(req_name)
            case ('delete',req_name):
                return delete_info_req(req_name)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_contact_action
    )

def edit_task_def_triggers(model_store: ModelStore, model_id: ModelID, task_id: TaskID, path_var: TaskVariable[str]):
    
    def create_trigger():
    
        def edit(value, errors):
            editor = BulmaTextInput(label='Name', help = (errors['name'],'danger') if 'name' in errors else None)         
            return update_information(value, editor=editor)
    
        def verify(value):
            if value is None or value == '':
                return constant({'name':'Name may not be empty'})
            return constant({})

        def save(value):
            return write_information(model_store, lambda ms: ms.task_def_create_trigger(model_id,task_id,value))
  
        return edit_in_dialog('Add trigger',constant(None),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def delete_trigger(name: str):
        return write_information(model_store, lambda ms: ms.task_def_delete_trigger(model_id,task_id,name))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add trigger','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.task_def_triggers(model_id,task_id),
                choose_list_action_with_triggers)

        def choose_list_action_with_triggers(triggers: list[Trigger]):

            headers = ['Reference']
            buttons = [BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')]

            options = [(trigger.reference,[trigger.reference],buttons) for trigger in triggers]
            
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
                return create_trigger()
            case ('delete',name):
                return delete_trigger(name)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_contact_action
    )

def edit_task_def_contraints(model_store: ModelStore, model_id, task_id):
    def view():
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor', disabled= True)),
            ('at_location',BulmaTextInput(label = 'At location', disabled = True))
        ])
        return view_information(model_store,lambda ms:ms.task_def_constraints(model_id, task_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor')),
            ('at_location',BulmaTextInput(label = 'At location'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ms:ms.write_task_def_constraints(model_id,task_id,updated_fields))

    return view_with_edit(view(),edit,save)

def view_task_def_source(model_store: ModelStore, model_id: ModelID, task_id: TaskID, path_var: TaskVariable[str]):
   
    def view():
        return view_information(model_store,lambda ms: ms.task_def_source(model_id,task_id),editor=SourceView())
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return write_information(model_store,lambda ms: ms.write_task_def_source(model_id,task_id,value))
    
    def save(value):
        return after_task(write_information(model_store,lambda ms: ms.write_task_def_source(model_id,task_id,value)),
            lambda node_id: constant(None)
            if node_id == task_id else (write_information(path_var,lambda pv:pv.write(task_def_node_path(model_id,node_id))))
        )
    
    def task_def_node_path(model_id, node_id):
        return f'/model/{model_id}' if node_id is None else f'/model/{model_id}/td/{node_id}'
        
    return view_with_edit(view(),edit,save)