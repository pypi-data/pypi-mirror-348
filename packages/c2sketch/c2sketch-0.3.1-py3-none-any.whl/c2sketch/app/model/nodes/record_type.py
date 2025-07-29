
from typing import Callable, Any

from toppyt import (TaskVariable, TaskStatus, TaskResult, ParallelTask, after_task, after_value, all_tasks, any_task, constant,
                    enter_information, forever,
                    map_value, update_information, view_information,
                    with_information, with_dependent, read_information, write_information)
from toppyt.bulma import (BulmaButtons, BulmaRecordEditor, BulmaSelect,
                          BulmaTextInput, BulmaTextArea, BulmaButtonSpec, BulmaTable)
from toppyt.patterns import edit_in_dialog, continuous_choice

from c2sketch.models import *
from c2sketch.app.data import ModelStore
from c2sketch.app.patterns import choose_task, view_with_edit
from c2sketch.app.ui import TableChoice, SourceView, SourceEditor, after_dialog, view_title

__all__ = ('edit_type_node',)

def edit_type_node(model_store: ModelStore, model_id: ModelID, type_id: RecordTypeID, path_var):
    def choose(general):
        if general is None:
            return view_information(f'Type "{type_id}" does not exist.')

        def layout(parts,task_tag):
            return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
        
        return ParallelTask ([
            ('title',view_title(type_id)),
            ('main',choose_task([
                ('Attributes','file-alt', edit_record_type_attributes(model_store, model_id, type_id)),
                ('Fields','puzzle-piece', edit_record_type_fields(model_store, model_id, type_id, path_var)),
                ('Source','code', edit_record_type_source(model_store,model_id,type_id,path_var)),
            ],'Fields'))
        ],layout=layout)
    return with_information(model_store,lambda ps:ps.record_type_attributes(model_id,type_id),choose,refresh=False)

def edit_record_type_attributes(model_store: ModelStore, model_id: ModelID, type_id: RecordTypeID):
    
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title', disabled = True)),
            ('description',BulmaTextArea(label= 'Description', disabled = True))
        ])
        return view_information(model_store,lambda ps: ps.record_type_attributes(model_id, type_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title')),
            ('description',BulmaTextArea(label = 'Description'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ps:ps.write_record_type_attributes(model_id, type_id,updated_fields))

    return view_with_edit(view(),edit,save)

def edit_record_type_fields(model_store: ModelStore, model_id: ModelID, type_id: TaskID, path_var: TaskVariable[str]):
    
    primitive_types = ['string','text','integer','float','boolean','byte','timestamp','latlng']

    def create_field():
        
        def edit(value, errors):   
            name_editor = BulmaTextInput(label='Name', help = (errors['name'],'danger') if 'name' in errors else None)
            type_editor = BulmaSelect(options=primitive_types, label='Type', help = (errors['type'],'danger') if 'type' in errors else None)
            
            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('type',type_editor)
            ])
            return update_information(value, editor=editor)
    
        def verify(value):
            if 'name' not in value or value['name'] is None or value['name'] == '':
                return constant({'name':'Name may not be empty'})
            return constant({})

        def save(value):
            name = value.get('name')
            type = None if 'type' not in value or value['type'] == '' else value['type']
            return write_information(model_store, lambda ms: ms.record_type_create_field(model_id,type_id,name,type))
  
        return edit_in_dialog('Add field',constant({}),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def update_field(field_name:str):
        def load():
            async def read(ms: ModelStore):
                field = await ms.record_type_get_field(model_id,type_id,field_name)
                value = {'name': field_name}
                if field.type is not None:
                    value['type'] = field.type
                return value 
            return read_information(model_store, read)
               
        def edit(value, errors):
            name_editor = BulmaTextInput(label='Name',disabled=True)
            type_editor = BulmaSelect(options = primitive_types, label='Type', help = (errors['type'],'danger') if 'type' in errors else None)

            editor = BulmaRecordEditor([
                ('name',name_editor),
                ('type',type_editor)
            ])
            return update_information(value, editor=editor)
        
        def verify(value):
            return constant({})
        
        def save(value):
            name = value.get('name')
            type = None if 'type' not in value or value['type'] == '' else value['type']
            
            return write_information(model_store, lambda ms: ms.record_type_update_field(model_id,type_id,name,type))
  
        return edit_in_dialog('Edit field',load(),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])
    
    def delete_field(field_name: str):
        return write_information(model_store, lambda ms: ms.record_type_delete_field(model_id,type_id,field_name))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add field','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.record_type_fields(model_id,type_id),
                choose_list_action_with_fields)

        def choose_list_action_with_fields(reqs: list[RecordTypeField]):

            headers = ['Name','Type']
            buttons = [BulmaButtonSpec('edit','Edit','edit',is_compact=True)
                      ,BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')
                      ]

            options = [(req.name,
                        [req.name,
                         req.type,
                         ]
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
                return create_field()
            case ('edit',field_name):
                return update_field(field_name)
            case ('delete',field_name):
                return delete_field(field_name)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_contact_action
    )


def edit_global_type(model_store: ModelStore, plan_id, type_name):
    def write_task(fields):
        return write_information(model_store,lambda ps:ps.write_type_fields(plan_id,type_name,fields))

    return edit_type_fields(model_store, lambda ms:ms.record_type_fields(plan_id,type_name), lambda x: x, write_task)

def edit_local_type(planstore: ModelStore, plan_id: ModelID, read_fun: Callable[[ModelStore],Any], write_task: Callable[[RecordType],Task]):

    def edit(global_types, local_type):
        if isinstance(local_type,RecordType):
            type_choice = '_custom_'
        elif isinstance(local_type,str):
            type_choice = local_type
        else:
            type_choice = None

        options = [('Custom...','_custom_')] + global_types

        def edit_details(choice):
            if choice != type_choice:
                if choice == '_custom_':
                    return write_task(RecordType(None,'_custom_',[]))
                else:
                    return write_task(choice)
                
            if choice == '_custom_':
                def write_fields(fields):
                    return write_task(RecordType(None, '_custom_',fields))
                return edit_type_fields(planstore,read_fun,lambda m: m.fields,write_fields)
            
            return view_information('')

        return with_dependent(update_information(type_choice,editor=BulmaSelect(options,label='Type',sync=True)),edit_details)

    return with_information(planstore, lambda ps:ps.read_list_type_options(plan_id),
        lambda global_types: with_information(planstore,read_fun,lambda t: edit(global_types,t))
    )
  
def edit_type_fields(store: ModelStore, read_fun, read_transform, write_task):

    def edit(fields):
        return forever([after_value(choose_action(fields),lambda r: do_action(fields,*r))])
    
    def choose_action(fields):
        headers = ['Field name','Field type','Optional','Possible values','Description']
        options = [(n,[f.name,f.type,'-','-'],[('edit','Edit','edit'),('delete','Delete','trash')]) for (n,f) in enumerate(fields)]
        actions = [('add','Add field','plus')]
        return any_task(
            enter_information(editor=TableChoice(options,headers)),
            map_value(enter_information(editor=BulmaButtons(actions,align='right')),lambda c: (None,c))
        )
    
    def field_to_dict(field:RecordTypeField):
        raw = dict()
        raw['name'] = field.name
        raw['type'] = field.type.value
        raw['optional'] = 'yes' if field.optional else 'no'
        raw['choices'] = '' if field.choices is None else ', '.join(field.choices)
        raw['description'] = '' if field.description is None else field.description
        return raw

    def field_from_dict(raw):
        name = raw.get('name')
        if name is None or name == '':
            name = 'untitled'
        type = raw.get('type','string')
        type = 'string' if type is None else type
        optional = raw.get('optional','no') == 'yes'
        choices = raw.get('choices','')
        if choices == '':
            choices = None
        else:
            choices = [c.strip() for c in choices.split(',')]
        description = raw.get('description')
        if description == '':
            description = None
        return RecordTypeField(name,type,optional,choices,description)
    
    def do_action(fields, subject, action):
        if action == 'add':
            return after_dialog('Add field..',
                lambda task, validate: edit_field(None,task,validate),
                lambda validate, task: constant(dict()),
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('add','Add','plus', lambda v: add_field(fields,v))
                ])

        if action == 'edit':
            field_no = int(subject)
            return after_dialog('Edit field..',
                lambda task, validate: edit_field(fields[field_no],task,validate),
                lambda validate, task: constant(dict()),
                [('cancel','Cancel','ban',lambda _: constant(None))
                ,('add','Save','save', lambda v: update_field(fields,field_no,v))
                ])
        if action == 'delete':
            field_no = int(subject)
            return delete_field(fields,field_no)

        return constant(None)

    def edit_field(default_field, value, validate):
        editor_value = value

        if default_field is not None and validate is None:
            editor_value = field_to_dict(default_field)

        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label='Field name')),
            ('type',BulmaSelect(['string','integer'],allow_empty=False,label='Field type')),
            ('optional',BulmaSelect(['no','yes'],allow_empty=False,label='Optional')),
            ('choices', BulmaTextInput(label='Choices')),
            ('description',BulmaTextInput(label='Description'))
        ])

        return update_information(editor_value,editor=editor)
    
    def add_field(fields,new_field):
        return write_task(fields + [field_from_dict(new_field)])

    def update_field(fields,field_no,updated_field):
        fields = [field_from_dict(updated_field) if i == field_no else field for i, field in enumerate(fields)]
        return write_task(fields)

    def delete_field(fields,field_no):
        fields = [field for i, field in enumerate(fields) if i != field_no]
        return write_task(fields)

    return with_information(store,read_fun,lambda r: edit(read_transform(r)))

def edit_record_type_source(model_store: ModelStore, model_id: ModelID, task_id: TaskID, path_var: TaskVariable[str]):
    
    def view():
        return view_information(model_store,lambda ms: ms.record_type_source(model_id,task_id),editor=SourceView())
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return after_task(write_information(model_store,lambda ms: ms.write_record_type_source(model_id,task_id,value)),
            lambda node_id: constant(None)
            if node_id == task_id else (write_information(path_var,lambda pv:pv.write(type_node_path(model_id,node_id))))
        )
    
    def type_node_path(model_id, node_id):
        return f'/model/{model_id}' if node_id is None else f'/model/{model_id}/m/{node_id}'
    
    return view_with_edit(view(),edit,save)