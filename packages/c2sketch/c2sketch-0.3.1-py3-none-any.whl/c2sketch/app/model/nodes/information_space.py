
from toppyt import (ParallelTask, TaskVariable, TaskStatus, TaskResult, after_task, after_value,
                    all_tasks, any_task, constant,
                    enter_information, forever, map_value,
                    read_information, update_information, view_information,
                    with_information, with_dependent, write_information, ViewEditor)
from toppyt.bulma import (BulmaButtons, BulmaIntInput, BulmaRecordEditor,
                          BulmaSelect, BulmaTextArea, BulmaTextInput, BulmaButtonSpec, BulmaTable)

from toppyt.patterns import continuous_choice, edit_in_dialog
from functools import partial

from c2sketch.models import *
from ...data import ModelStore
from ...patterns import choose_task, view_with_edit
from ...plugins import AppPluginLoader
from ...ui import (TableChoice, SourceView, SourceEditor, after_dialog, record_editor, record_view,
                  view_title)

def edit_info_space_node(model_store: ModelStore, visualizations, model_id: ModelID, ifs_id: InformationSpaceID, path_var: TaskVariable):
    def choose(general):
        if general is None:
            return view_information(f'Information space "{ifs_id}" does not exist.')

        def layout(parts,task_tag):
            return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
   
        return ParallelTask ([
            ('title',view_title(general['name'])),
            ('main',choose_task([
            ('Attributes','file-alt', edit_info_space_attributes(model_store, model_id,ifs_id)),
            ('Records','envelope', edit_info_space_records(model_store, model_id, ifs_id, path_var)),
            ('Visualization','image', view_info_space_visualization(model_store, visualizations, model_id,ifs_id)),
            ('Constraints','ban',edit_info_space_contraints(model_store, model_id, ifs_id)),
            ('Source','code', edit_info_space_source(model_store,model_id,ifs_id,path_var)),
            ],'Attributes'))
        ],layout=layout)
    return with_information(model_store,lambda ps:ps.info_space_attributes(model_id,ifs_id),choose,refresh=False)

def edit_info_space_attributes(model_store: ModelStore, model_id: ModelID, ifs_id: InformationSpaceID):
   
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('type',BulmaTextInput(label='Type',disabled=True)),
            ('title',BulmaTextInput(label = 'Title', disabled = True)),
            ('description',BulmaTextArea(label= 'Description', disabled = True)) 
        ])
        return view_information(model_store,lambda ps: ps.info_space_attributes(model_id, ifs_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('type',BulmaTextInput(label='Type')),
            ('title',BulmaTextInput(label = 'Title')),
            ('description',BulmaTextArea(label = 'Description'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ps:ps.write_info_space_attributes(model_id, ifs_id,updated_fields))

    return view_with_edit(view(),edit,save)

def edit_info_space_records(model_store: ModelStore, model_id: ModelID, ifs_id: InformationSpaceID, path_var: TaskVariable[str]):
    
    def create_record(record_type: RecordType | None):
        if record_type is None:
            return constant(None)
        
        def edit(value, errors):   
            editor = record_editor(record_type)
            return update_information(value, editor=editor)
    
        def verify(value):
            return constant({})

        def save(value):
            return write_information(model_store, lambda ms: ms.info_space_create_record(model_id,ifs_id,value))
  
        return edit_in_dialog('Add record',constant({}),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def update_record(record_type: RecordType | None, seq_nr:int):

        def load():
            async def read(ms:ModelStore):
                record = await ms.info_space_get_record(model_id,ifs_id,seq_nr)
                return record.fields
            return read_information(model_store, read)
               
        def edit(value, errors):
          
            editor = record_editor(record_type)
            return update_information(value, editor=editor)
        
        def verify(value):
            return constant({})
        
        def save(value):
            return write_information(model_store, lambda ms: ms.info_space_update_record(model_id,ifs_id,seq_nr,value))
  
        return edit_in_dialog('Edit Record',load(),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])
    
    def delete_record(seq_nr: int):
        return write_information(model_store, lambda ms: ms.info_space_delete_record(model_id,ifs_id,seq_nr))

    def select_action(record_type: RecordType | None):

        if record_type is None:
            return constant(None)

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add Record','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.info_space_records(model_id,ifs_id),
                choose_list_action_with_records)

        def choose_list_action_with_records(records: list[Record]):

            headers = ['#',*(field.name for field in record_type.fields)]
            def row(record:Record):
                return [record.sequence_number,*(record.fields[field.name] if field.name in record.fields else '-' for field in record_type.fields)]
            
            buttons = [BulmaButtonSpec('edit','Edit','edit',is_compact=True)
                      ,BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')
                      ]
            options = [(record.sequence_number,row(record),buttons) for record in records]

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

    def handle_record_action(record_type, action):
        match action:
            case ('create',):
                return create_record(record_type)
            case ('edit',record_index):
                return update_record(record_type, int(record_index))
            case ('delete',record_index):
                return delete_record(int(record_index))
          
        return constant(None)
 
    return with_information(model_store,lambda ms:ms.info_space_type(model_id,ifs_id,True),lambda type:
                            continuous_choice(lambda _ :select_action(type),partial(handle_record_action,type)))
   

def view_info_space_visualization(model_store: ModelStore, plugins: AppPluginLoader, model_id: ModelID, ifs_id: InformationSpaceID):
    
    def view(mb_plugin):
        if mb_plugin is None:
            return view_information('No visualization configured')
        
        if mb_plugin not in plugins.info_space_graphics:
            return view_information('Unknown visualization plugin')
        else:
            plugin_cls = plugins.info_space_graphics[mb_plugin]
            plugin = plugin_cls()
            models = model_store.model_set #FIXME: No direct access
            time = 0
            plugin.start(time,global_id_from_id(ifs_id,model_id),models)

            editor = ViewEditor(lambda records: plugin.render_svg(time,records))

        return view_information(model_store, lambda ms:ms.info_space_records(model_id,ifs_id),editor=editor)

    return with_information(model_store,lambda es:es.info_space_graphic_type(model_id,ifs_id),view)


def edit_info_space_contraints(model_store: ModelStore, model_id, ifs_id):
    def view():
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor', disabled= True)),
            ('at_location',BulmaTextInput(label = 'At location', disabled = True))
        ])
        return view_information(model_store,lambda ms:ms.info_space_constraints(model_id, ifs_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('for_actor',BulmaTextInput(label = 'For actor')),
            ('at_location',BulmaTextInput(label = 'At location'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ms:ms.write_info_space_constraints(model_id,ifs_id,updated_fields))

    return view_with_edit(view(),edit,save)

def edit_info_space_source(model_store: ModelStore, model_id: ModelID, ifs_id: InformationSpaceID, path_var: TaskVariable[str]):
    
    def view():
        return view_information(model_store,lambda ms: ms.info_space_source(model_id,ifs_id),editor=SourceView())
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return after_task(write_information(model_store,lambda ms: ms.write_info_space_source(model_id,ifs_id,value)),
            lambda node_id: constant(None)
            if node_id == ifs_id else (write_information(path_var,lambda pv:pv.write(ifs_node_path(model_id,node_id))))
        )
    
    def ifs_node_path(model_id, node_id):
        return f'/model/{model_id}' if node_id is None else f'/model/{model_id}/i/{node_id}'
    
    return view_with_edit(view(),edit,save)