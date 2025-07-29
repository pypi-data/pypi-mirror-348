"""Structural edits such as creating, renaming and deleting nodes"""

from toppyt import (ParallelTask, all_tasks, constant, map_value, forever,
                    read_information, update_information,
                    view_information, write_information, with_information)
from toppyt.bulma import (BulmaRecordEditor, BulmaSelect, BulmaTextArea,
                          BulmaTextInput, BulmaButtonSpec)

from toppyt.patterns import edit_in_dialog, view_in_dialog

from c2sketch.models import *
from ..config import AppConfig
from ..data import ModelStore
from ..ui import *
from ..patterns import action_choice


from .nodes.actor import edit_actor_node
from .nodes.location import edit_location_node
from .nodes.task import edit_task_node
from .nodes.task_definition import edit_task_def_node
from .nodes.task_instance import edit_task_instance_node
from .nodes.information_space import edit_info_space_node
from .nodes.record_type import edit_type_node
from .nodes.model import edit_model_node

from functools import partial

__all__ = ('edit_model','edit_node')

def edit_model(config: AppConfig, model_store: ModelStore, plugins, model_id: ModelID, path_var, cookie_jar):
    return edit_node_in_context(config,model_store,plugins,model_id,path_var,cookie_jar, edit_model_node(model_store, model_id, path_var))

def edit_node(config: AppConfig, model_store: ModelStore, plugins, model_id: ModelID, node_type, node_id, path_var, cookie_jar):
    if node_type == 'a':
        node_task = edit_actor_node(model_store, model_id, node_id, path_var)
    elif node_type == 'l':
        node_task = edit_location_node(model_store, model_id, node_id, path_var)
    elif node_type == 't':
        node_task = edit_task_node(model_store, plugins, model_id, node_id, path_var)
    elif node_type == 'td':
        node_task = edit_task_def_node(model_store, model_id, node_id, path_var)
    elif node_type == 'ti':
        node_task = edit_task_instance_node(model_store, model_id, node_id, path_var)
    elif node_type == 'i':
        node_task = edit_info_space_node(model_store, plugins, model_id, node_id, path_var)
    elif node_type == 'm':
        node_task = edit_type_node(model_store, model_id, node_id, path_var)
    return edit_node_in_context(config,model_store,plugins,model_id,path_var,cookie_jar,node_task)

def edit_node_in_context(config: AppConfig, model_store: ModelStore, plugins, model_id: ModelID, path_var, cookie_jar, node_task):
    
    def edit(model: Model):
    
        return ParallelTask(
            [('subtitle',view_model_title(model.id, model.title, path_var))
            ,('choose_node',choose_node(model_store, model.id, path_var))
            ,('edit_outline',edit_outline(model_store, model.id, path_var))
            ,('edit_node',node_task)
            ,('app_mode',choose_app_mode(path_var))
            ],layout=partial(edit_model_layout,config.name),result_builder=lambda rs:rs[-1])
    
    return with_information(model_store,lambda ps:ps.model(model_id),edit,refresh=False)

def edit_model_layout(title, parts, task_tag):
    
    header = model_header(title=title, actor_location=parts['subtitle'],app_mode=parts['app_mode'])

    return f'''
        <div {task_tag} class="prepare-grid">
            <div class="prepare-header">{header}</div>
            <div class="prepare-body">
                <div class="prepare-side">
                    <div class="panel-block buttons">
                    {parts['edit_outline']}
                    </div>
                    <div class="panel-block">
                    {parts['choose_node']}
                    </div>
                </div>
                <flex-resizer></flex-resizer>
                <div class="prepare-main">
                <div class="container prepare-inner">
                {parts['edit_node']}
                </div>
                </div>
            </div>
        </div>
    '''


def edit_outline(model_store: ModelStore, model_id: ModelID, path_var: TaskVariable[str]):

    def edit(path: str):
        path_segments = path.split('/')
        node_type = path_segments[3] if len(path_segments) >= 4 else None
        node_id = path_segments[4] if len(path_segments) >= 5 else None
    
        actions = [
            ('add','Add...','plus',add_node(model_store,model_id,node_type,node_id)),
            ('delete','Delete...','trash',delete_node(model_store,model_id,node_type,node_id,path_var))
            ]
        return forever(action_choice(actions))
    
    return with_information(path_var, lambda pv: pv.read(), edit)


def choose_node(model_store: ModelStore, model_id, path_var):
    def model_nodes(model: Model | None):
        if model is None:
            return []

        def to_tree_nodes(nodes: list[Node]):
            result = []
            for node in nodes:
                match node:
                    case Actor():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name,'icon': 'user','value': f'/model/{model.id}/a/{node_id}'})
                    case Location():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name,'icon':'map-pin','value':f'/model/{model.id}/l/{node_id}'})
                    case Task():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name, 'icon': 'check','value': f'/model/{model.id}/t/{node_id}','children': to_tree_nodes(node.nodes)})
                    case TaskDefinition():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name, 'icon': 'check-double','value': f'/model/{model.id}/td/{node_id}','children': to_tree_nodes(node.nodes)})
                    case TaskInstance():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': f'{node.name}-{node.sequence}', 'icon': 'circle-check','value': f'/model/{model.id}/ti/{node_id}','children': to_tree_nodes(node.nodes)})
                    case InformationSpace():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name, 'icon': 'chalkboard','value': f'/model/{model.id}/i/{node_id}'})
                    case RecordType():
                        node_id = local_id_from_global_id(node.node_id)[0]
                        result.append({'name': node.name, 'icon':'puzzle-piece','value': f'/model/{model.id}/m/{node_id}'})
            return result
               
        return [{'name': model.id,'icon':'sitemap'
                 ,'value': f'/model/{model.id}'
                 ,'children': to_tree_nodes(model.nodes)}]
    
    return with_information(model_store, lambda ms:ms.model(model_id),
        lambda model: update_information(path_var, editor=TreeChoice(model_nodes(model)))
    )

def parent_options(plan:Model) -> list[tuple[str,str]]:
    options: list[tuple[str,str]] = []
    
    def add_task(prefix: list[str], task: Task,options):
        path = prefix + [task.name]
        options.append(('.'.join(path),task.node_id))
        for part in task.tasks:
            add_task(path,part,options)

    for task in plan.tasks:
        add_task([],task,options)
    
    return options


#Pure check for node names
def validate_name(errors, name):
    if name is None or name == '':
        errors['name'] = 'Name cannot be empty.'
    elif not is_safe_name(name):
        errors['name'] = 'Name may only contain alphanumeric characters or underscores.' 
    return errors

#Impure uniqueness checks need the model store
def validate_unique_actor(model_store: ModelStore, model_id: ModelID, errors, name):
    def check(exists):
        if exists:
            errors['name'] = f'An actor named \'{name}\' already exists.'
        return errors
    return map_value(read_information(model_store,lambda ms: ms.actor_exists(model_id, name)),check)

def validate_unique_location(model_store: ModelStore, model_id: ModelID, errors, name):
    def check(exists):
        if exists:
            errors['name'] = f'A location named \'{name}\' already exists.'
        return errors
    return map_value(read_information(model_store,lambda ms: ms.location_exists(model_id, name)),check)

def validate_unique_task(model_store: ModelStore, model_id, errors, name, parent):
    def check(exists):
        if exists:
            errors['name'] = f'A task named \'{name}\' already exists as part of \'{parent}\'.'
        return errors
    task_id = name if parent is None else child_id(parent,name)
    return map_value(read_information(model_store,lambda ms:ms.task_exists(model_id, task_id)),check)

def validate_unique_task_def(model_store: ModelStore, model_id, errors, name, parent):
    def check(exists):
        if exists:
            errors['name'] = f'A task definition named \'{name}\' already exists as part of \'{parent}\'.'
        return errors
    task_id = name if parent is None else child_id(parent,name)
    return map_value(read_information(model_store,lambda ms:ms.task_definition_exists(model_id, task_id)),check)

def validate_unique_info_space(model_store: ModelStore, model_id, errors, name):
    def check(exists):
        if exists:
            errors['name'] = f'An information space named \'{name}\' already exists.'
        return errors
    return map_value(read_information(model_store,lambda ps:ps.info_space_exists(model_id,name)),check)

def validate_unique_record_type(model_store: ModelStore, model_id, errors, name):
    def check(exists):
        if exists:
            errors['name'] = f'A record type named \'{name}\' already exists.'
        return errors
    return map_value(read_information(model_store,lambda ps:ps.record_type_exists(model_id, name)),check)

def add_node(model_store: ModelStore, model_id, node_type, node_id):

    actor_types = [
        ('Person','person'),
        ('Organization','organization'),
        ('Team','team'),
        ('Machine','machine'),
    ]

    def load():
        suggestions = {'a':'Actor','l':'Location','t':'Task','td':'Task Definition','ti':'Task Instance','i':'Information Space','m':'Record Type'}
        if node_type is None:
            return constant((None,None))
        else:
            return constant((suggestions[node_type],None))
    
    def edit(task, validate):
        return with_information(model_store,lambda ps:ps.model(model_id),
            lambda model: enter_options(model,task,validate),refresh = False)
 
    def enter_options(model, value, validate):
        type_value, detail_value = (None, None) if value is None else value

        def choose_type(type_value):
            help = None
            if validate is not None and 'type' in validate:
                help = (validate['type'],'danger')

            editor = BulmaSelect(['Actor','Location','Task','Task Definition','Task Instance','Information Space','Record Type'], sync = True,help=help)
            return update_information(type_value,editor=editor)
        
        def enter_details(type):
            help = {}
            for field_name in ['name','type','title','description','parent']:
                if validate is not None and field_name in validate:
                    help[field_name] = (validate[field_name],'danger')
                else:
                    help[field_name] = None

            if type == 'Actor':
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('title',BulmaTextInput(label='Title',help=help['description'])),
                    ('description',BulmaTextArea(label='Description',help=help['description'])),
                    ('type',BulmaSelect(actor_types,label='Type'))
                ]
                if detail_value is None:
                    editor_value = {'name':None,'title':None,'description':None}
                else:
                    editor_value = detail_value
            elif type == 'Location':
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('title',BulmaTextInput(label='Title',help=help['description'])),
                    ('description',BulmaTextArea(label='Description',help=help['description']))
                ]
                if detail_value is None:
                    editor_value = {'name':None,'title':None,'description':None}
                else:
                    editor_value = detail_value
            elif type == 'Task':
                parent_nodes = parent_options(model)
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('title',BulmaTextInput(label='Title',help=help['description'])),
                    ('description',BulmaTextArea(label='Description',help=help['description'])),
                    ('parent',BulmaSelect(parent_nodes,label='As part of', disabled = False,help=help['parent']))
                ]
                if detail_value is None:
                    suggested_parent = parent_from_id(node_id) if node_type in ['t','td','ti'] else None
                    editor_value = {'name':None,'title':None,'description':None,'parent':suggested_parent}
                else:
                    editor_value = detail_value

            elif type == 'Task Definition':
                parent_nodes = parent_options(model)
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('type',BulmaTextInput(label='Type',help=help['type'])),
                    ('title',BulmaTextInput(label='Title',help=help['description'])),
                    ('description',BulmaTextArea(label='Description',help=help['description'])),
                    ('parent',BulmaSelect(parent_nodes,label='As part of', disabled = False,help=help['parent']))
                ]
                if detail_value is None:
                    suggested_parent = parent_from_id(node_id) if node_type in ['t','td','ti'] else None
                    editor_value = {'name':None,'type': None, 'title':None,'description':None,'parent':suggested_parent}
                else:
                    editor_value = detail_value

            elif type == 'Task Instance':
                parent_nodes = parent_options(model)
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('title',BulmaTextInput(label='Title',help=help['description'])),
                    ('description',BulmaTextArea(label='Description',help=help['description'])),
                    ('parent',BulmaSelect(parent_nodes,label='As part of', disabled = False,help=help['parent']))
                ]
                if detail_value is None:
                    suggested_parent = parent_from_id(node_id) if node_type in ['t','td','ti'] else None
                    editor_value = {'name':None,'title':None,'description':None,'parent':suggested_parent}
                else:
                    editor_value = detail_value
            elif type == 'Information Space':
                parent_nodes = parent_options(model)
                info_space_type_options = []
                fields = [
                    ('name',BulmaTextInput(label='Name',help=help['name'])),
                    ('title',BulmaTextInput(label='Title',help=help['title'])),
                    ('description',BulmaTextArea(label='Description',help=help['description'])),
                    ('type',BulmaSelect(info_space_type_options,label='Type'))
                ]
                if detail_value is None:
                    editor_value = {'name':None,'title':None,'description':None,'type':None}
                else:
                    editor_value = detail_value
            elif type == 'Record Type':
                fields = [('name',BulmaTextInput(label='Name',help=help['name']))]
                if detail_value is None:
                    editor_value = {'name':None}
                else:
                    editor_value = detail_value
            else:
                fields = []
                editor_value = None
            return update_information(editor_value, editor=BulmaRecordEditor(fields))
            
        return ParallelTask([
            ('type',choose_type(type_value)),
            ('details',[('type',type_value)], lambda type: enter_details(type.value))
        ],result_builder=lambda rs: TaskResult([r.value for r in rs], TaskStatus.ACTIVE))

 
    def validate(value):
        errors = {}

        if value is None:
            node_type, options = None, None
        else:
            node_type, options = value

        #First check all pure properties
        if node_type is None:
            errors['type'] = 'Node type cannot be empty.'
        else:
            if options is not None:
                validate_name(errors, options.get('name')) 
    
        #If name is ok, check uniqueness of the new node
        if not 'name' in errors and not 'parent' in errors:
            if node_type == 'Actor':
                return validate_unique_actor(model_store, model_id, errors,options['name'])
            if node_type == 'Location':
                return validate_unique_location(model_store, model_id, errors, options['name'])
            if node_type == 'Task':
                return validate_unique_task(model_store, model_id, errors,options['name'],options['parent'])
            if node_type == 'Task Definition':
                return validate_unique_task_def(model_store, model_id, errors,options['name'],options['parent'])
            if node_type == 'Information Space':
                return validate_unique_info_space(model_store, model_id, errors,options['name'])
            if node_type == 'Record Type':
                return validate_unique_record_type(model_store, model_id, errors,options['name'])
        
        return constant(errors)
   
    def save(options):
        if options[0] == 'Actor' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_actor(model_id,options[1]['name'],options[1]['title'],options[1]['description'],options[1]['type']))
        if options[0] == 'Location' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_location(model_id,options[1]['name'],options[1]['title'],options[1]['description']))
        if options[0] == 'Task' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_task(model_id,options[1]['parent'],options[1]['name'],options[1]['title'],options[1]['description']))
        if options[0] == 'Task Definition' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_task_definition(model_id,options[1]['parent'],options[1]['name'],options[1]['type'],options[1]['title'],options[1]['description']))
        if options[0] == 'Task Instance' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_task_instance(model_id,options[1]['parent'],options[1]['name'],options[1]['title'],options[1]['description']))
        if options[0] == 'Information Space' and options[1]['name'] is not None:
            return write_information(model_store,lambda ms:ms.create_info_space(model_id,options[1]['name'],options[1]['title'],options[1]['description'],options[1]['type']))
        if options[0] == 'Record Type' and options[1] is not None:
            return write_information(model_store,lambda ms:ms.create_record_type(model_id,options[1]['name']))
        return constant(None)

    return edit_in_dialog('Add...',
        load(),
        edit,
        validate,
        [(BulmaButtonSpec('cancel','Cancel','ban'), False, lambda _: constant(None))
        ,(BulmaButtonSpec('add','Add','plus'), True,save)
        ]
        )

def delete_node(model_store: ModelStore, model_id: ModelID, node_type: str | None, node_id: str | None, path_var: TaskVariable[str]):
    
    if node_type is None or node_id is None:
        return constant(None)

    def view():
        messages = {
            'a': f'Are you sure you want to delete actor "{node_id}"?',
            'l': f'Are you sure you want to delete location "{node_id}"?',
            't': f'Are you sure you want to delete task "{node_id}"?',
            'td': f'Are you sure you want to delete task definition "{node_id}"?',
            'ti': f'Are you sure you want to delete task instance "{node_id}"?',
            'i': f'Are you sure you want to delete information space "{node_id}"?',
            'm': f'Are you sure you want to delete record type "{node_id}"?'
        }
        return view_information(f'{messages[node_type]} This cannot be undone.')

    def save():
        if node_type in ['t','i']:
            parent = parent_from_id(node_id)
            if parent is not None:
                new_path = f'/model/{model_id}/t/{parent_from_id(node_id)}'
            else:
                new_path = f'/model/{model_id}'         
        else:
            new_path = f'/model/{model_id}'

        actions = {'a':lambda ms:ms.delete_actor(model_id,node_id),
                   'l':lambda ms:ms.delete_location(model_id,node_id),
                   't':lambda ms:ms.delete_task(model_id,node_id),
                   'td':lambda ms:ms.delete_task_definition(model_id,node_id),
                   'ti':lambda ms:ms.delete_task_instance(model_id,node_id),
                   'i':lambda ms:ms.delete_info_space(model_id,node_id),
                   'm':lambda ms:ms.delete_record_type(model_id,node_id)} 
        return all_tasks(
            write_information(model_store, actions[node_type]),
            write_information(path_var,lambda pv:pv.write(new_path))
        )
      
    return view_in_dialog('Delete..',
        constant(None),
        lambda _ : view(),
        [(BulmaButtonSpec('cancel','Cancel','ban'),False,lambda _: constant(None))
        ,(BulmaButtonSpec('delete','Delete','check'),False,lambda _: save())
        ])
