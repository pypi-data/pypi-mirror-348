__all__ = ('edit_location_node',)

from toppyt import ParallelTask, TaskStatus, TaskResult, view_information, enter_information, all_tasks, with_information, update_information, write_information, constant, after_task, TaskVariable
from toppyt.bulma import BulmaTextInput, BulmaTextArea, BulmaRecordEditor, BulmaButtonSpec, BulmaTable, BulmaButtons
from toppyt.patterns import edit_in_dialog, continuous_choice
from ...ui import SourceView, SourceEditor, view_title
from ...patterns import choose_task, view_with_edit
from ...data import ModelStore
from c2sketch.models import ModelID, LocationID

def edit_location_node(model_store: ModelStore, model_id, location_id, path_var):
    
    def choose(general):
        if general is None:
            return view_information(f'Location "{location_id}" does not exist.')
        
        def layout(parts,task_tag):
            return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
        
        return ParallelTask ([
            ('title',view_title(general['name'])),
            ('main',choose_task([
                ('Attributes','file-alt', edit_location_attributes(model_store, model_id, location_id)),
                ('Relations','map-pin',edit_location_relations(model_store, model_id, location_id, path_var)),
                ('Source','code', edit_location_source(model_store,model_id,location_id, path_var))
            ],'Attributes'))
        ],layout=layout)
    return with_information(model_store,lambda ps:ps.location_attributes(model_id,location_id),choose,refresh=False)

def edit_location_attributes(model_store, model_id, location_id):
    return view_information(location_id)

def edit_location_attributes(model_store: ModelStore, model_id: ModelID, location_id: LocationID):
    
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title', disabled = True)),
            ('description',BulmaTextArea(label= 'Description', disabled = True))
        ])
        return view_information(model_store,lambda ps: ps.location_attributes(model_id, location_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title')),
            ('description',BulmaTextArea(label = 'Description'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(model_store,lambda ps:ps.write_location_attributes(model_id, location_id,updated_fields))

    return view_with_edit(view(),edit,save)

def edit_location_relations(model_store: ModelStore, model_id, actor_id, path_var):  
    
    def layout(parts,task_tag):
        return f'''
        <div {task_tag}>
        <div class="content"><h2 class="is-size-4">Groups</h2></div>
        {parts['groups']}
        <div class="content"><h2 class="is-size-4">Members</h2></div>
        {parts['members']}
        </div>
        '''

    return ParallelTask([
        ('groups',edit_location_groups(model_store, model_id, actor_id)),
        ('members',edit_location_members(model_store, model_id, actor_id))
    ], layout = layout)


def edit_location_groups(model_store: ModelStore, model_id: ModelID, location_id: LocationID):  

    def create_group():
        def edit(value, errors):
            editor = BulmaTextInput(label='Group', help = (errors['group_id'],'danger') if 'group_id' in errors else None)         
            return update_information(value, editor=editor)
    
        def verify(value):
            if value is None or value == '':
                return constant({'group_id':'Group may not be empty'})
            return constant({})

        def save(value):
            return write_information(model_store, lambda ms: ms.location_create_group(model_id,location_id,value))
  
        return edit_in_dialog('Add group',constant(None),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def delete_group(group_id: LocationID):
        return write_information(model_store, lambda ms: ms.location_delete_group(model_id,location_id,group_id))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add group','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.location_groups(model_id,location_id),
                choose_list_action_with_groups)

        def choose_list_action_with_groups(groups: list[LocationID]):

            headers = ['Group']
            buttons = [BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')]

            options = [(group_id,[group_id],buttons) for group_id in groups]
            
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

    def handle_action(action):
        match action:
            case ('create',):
                return create_group()
            case ('delete',group_id):
                return delete_group(group_id)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_action
    )

def edit_location_members(model_store: ModelStore, model_id: ModelID, location_id: LocationID):  

    def create_member():
        def edit(value, errors):
            editor = BulmaTextInput(label='Member', help = (errors['member_id'],'danger') if 'member_id' in errors else None)         
            return update_information(value, editor=editor)
    
        def verify(value):
            if value is None or value == '':
                return constant({'member_id':'Member may not be empty'})
            return constant({})

        def save(value):
            return write_information(model_store, lambda ms: ms.location_create_member(model_id,location_id,value))
  
        return edit_in_dialog('Add member',constant(None),edit,verify,
            [(BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),False, lambda _ : constant(None))
            ,(BulmaButtonSpec('plus','Add','plus',is_enter=True,extra_cls='is-primary'),True,save)])

    def delete_member(member_id: LocationID):
        return write_information(model_store, lambda ms: ms.location_delete_member(model_id,location_id,member_id))

    def select_action():

        def choose_global_action():
            buttons = [BulmaButtonSpec('create','Add member','plus')]
            return enter_information(editor=BulmaButtons(buttons,align='right'))
        
        def choose_list_action():
            return with_information(model_store,
                lambda ms:ms.location_members(model_id,location_id),
                choose_list_action_with_members)

        def choose_list_action_with_members(members: list[LocationID]):

            headers = ['Member']
            buttons = [BulmaButtonSpec('delete','Delete','trash',is_compact=True,extra_cls='is-danger')]

            options = [(member_id,[member_id],buttons) for member_id in members]
            
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

    def handle_action(action):
        match action:
            case ('create',):
                return create_member()
            case ('delete',member_id):
                return delete_member(member_id)
          
        return constant(None)
 
    return continuous_choice(
        lambda _ :select_action(),
        handle_action
    )

def edit_location_source(model_store: ModelStore, model_id, actor_id, path_var: TaskVariable[str]):

    def view():
        return view_information(model_store,lambda ms: ms.location_source(model_id,actor_id),editor=SourceView())
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return after_task(write_information(model_store,lambda ms: ms.write_location_source(model_id,actor_id,value)),
            lambda node_id: constant(None)
            if node_id == actor_id else (write_information(path_var,lambda pv:pv.write(location_node_path(model_id,node_id))))
        )
    
    def location_node_path(model_id, node_id):
        return f'/model/{model_id}' if node_id is None else f'/model/{model_id}/l/{node_id}'
      
    return view_with_edit(view(),edit,save)