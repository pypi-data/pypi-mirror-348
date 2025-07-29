"""Creating, selecting and deleting models"""

from toppyt import TaskStatus, TaskResult, TaskVariable, ParallelTask, SequenceTask, forever, update_information,\
    with_dependent, enter_information, constant, with_information, with_download, write_information, view_information, sequence_tasks, progress_on_stable, all_tasks, ViewEditor
from toppyt.bulma import BulmaTextInput, BulmaSelect, BulmaRecordEditor, BulmaTextArea

from ..config import AppConfig
from ..data import ModelStore
from ..ui import TreeChoice, after_dialog, model_header, choose_app_mode, view_title
from ..patterns import action_choice

from c2sketch.models import *
from c2sketch.export import nx_full_network, model_to_docx

import html
import tempfile
import networkx as nx

def manage_models(config: AppConfig, model_store: ModelStore, path_var, cookie_jar):
    
    selection_var = TaskVariable(None)

    def select_model():
        def to_nodes(models):

            nodes = []
            for model_id, model_title, model_description in sorted(models,key=lambda e:e[0]):
                
                node_list = nodes
                segments = model_id.split('.')
                for segment in segments[:-1]:
                    if not node_list or node_list[-1]['name'] != segment:
                        node_list.append({'name': segment,'icon': 'folder','value': None,'children':[]})
                    node_list = node_list[-1]['children']
                
                node_list.append({'name': segments[-1],'icon': 'sitemap','value': model_id,'children':[]})
           
            return nodes

        return with_information(model_store, lambda ps:ps.list_models(),
            lambda models: update_information(selection_var, editor=TreeChoice(to_nodes(models)))
        )

    def view_details():
        
        def view(model_id: ModelID | None):
            if model_id is None or model_id == '':
                def html_rendering(value):
                    return  f'''
                    <h2 class="title">Model collection</h2>
                    <div class="content mb-3">
                    Select a model in the overview on the left or create a new model.
                    </div>
                    '''
                actions = [('add','Create...','plus',create_model(model_store, path_var))]
                return all_tasks (
                    view_information(None, editor=ViewEditor(html_rendering)),
                    forever(action_choice(actions,compact_buttons=False))
                )
            else:
                actions = [
                    ('edit','Edit...','edit',edit_model(model_id, path_var)),
                    ('export','Export...','download',export_model(model_store,model_id))
                    ]
                
                def html_rendering(attr: dict[str,str] | None):
                    if attr is None:
                        attr = {}
                    title = '' if attr.get("title") is None else attr.get("title")
                    summary = '' if attr.get("summary") is None else attr.get("summary")

                    return  f'''
                    <h2 class="title">{title}</h2>
                    <div class="content mb-3">
                    {html.escape(summary)}
                    </div>
                    '''
                
                return all_tasks (
                    view_information(model_store,lambda ps: ps.model_attributes(model_id), editor=ViewEditor(html_rendering)),
                    forever(action_choice(actions,compact_buttons=False))
                )
        
        return with_information(selection_var,lambda s: s.read(), view)
       
    
    def layout(parts, task_tag):
        return f'''
        <div {task_tag} class="prepare-grid">
            <div class="prepare-header">{model_header(config.name, 'Model','','',parts['app_mode'])}</div>
            <div class="prepare-body">
                <div class="prepare-side">
                    <div class="panel-block buttons">
                    {parts['model_actions']}
                    </div>
                    <div class="panel-block">
                    {parts['choose_model']}
                    </div>
                </div>
                <flex-resizer></flex-resizer>
                <div class="prepare-main">
                <div class="container prepare-inner">
                {parts['preview_model']}
                </div>
                </div>
            </div>
        </div>
        '''
    def select_action(model_id):
        selection = model_id is not None and model_id != ''
        actions = [
                ('create','Create...','plus',create_model(model_store,path_var)),
                ('edit','Edit...','edit',edit_model(model_id, path_var) if selection else None),
                ('delete','Delete...','trash',delete_model(model_store,model_id,path_var,selection_var) if selection else None)
                ]
        return forever(action_choice(actions))
    
    return ParallelTask(
        [('choose_model',select_model())
        ,('model_actions',with_information(selection_var,lambda s:s.read(), select_action))
        ,('preview_model',view_details())
        ,('app_mode',choose_app_mode(path_var))
        ],layout=layout,result_builder=lambda rs:rs[-1])

def create_model(model_store: ModelStore, path_var: TaskVariable[str]):
   
    def enter(task, validate):
        def enter_title(title):
            return update_information(title,editor=BulmaTextInput(label='Title',sync=True))            

        def enter_name(name, title, validate):
            help = None
            if validate is not None and 'name' in validate:
                help = (validate['name'],'danger')
            placeholder = to_safe_name('' if title.value is None else title.value)
            return update_information(name,editor=BulmaTextInput(placeholder=placeholder,help=help,label='Name'))
        
        def enter_parent(models, parent):
            options = [('None (top-level)','')] + [p[0] for p in models]
            return update_information(parent, editor=BulmaSelect(options, label='As part of',allow_empty=False))
          
        def result(results):
            names = ['title','name','parent']
            return TaskResult({k: r.value for k,r in zip(names,results)}, TaskStatus.ACTIVE)
    
        return with_information(model_store, lambda ps: ps.list_models(),lambda models: ParallelTask([
            ('title',enter_title(None if task is None else task.get('title'))),
            ('name','title',lambda title: enter_name(None if task is None else task.get('name'),title,validate)),
            ('parent',enter_parent(models, None if task is None else task.get('parent')))
        ],result_builder=result))
    
    def validate(value: dict[str,str], action):
        if action == 'cancel':
            return constant(dict())

        def check_input(existing_model_ids):
            errors = {}
            name = None if value is None else value.get('name','')
            parent = value.get('parent','')
            if name == '':
                name = to_safe_name(value.get('title',''))
        
            if name is not None and not is_safe_name(name):
                errors['name'] = 'Name is not a valid name. It may not contain spaces and cannot start with a number.'
            else:
                new_model_id = name if parent == '' else f'{parent}.{name}'
                if new_model_id in [item[0] for item in existing_model_ids]:
                    if parent == '':
                        errors['name'] = f'A model named \'{name}\' already exists.'
                    else:
                        errors['name'] = f'A model named \'{name}\' already exists as part of \'{parent}\'.'

            return constant(errors)
        
        return with_information(model_store, lambda ms: ms.list_models(),check_input,refresh=False)
   
    def save(options):
        title = options.get('title','')
        if title == '':
            title = None
        name = options.get('name','')
        if name == '':
            name = to_safe_name('' if title is None else title)
        parent_id = options.get('parent','')
        model_id = name if parent_id == '' else f'{parent_id}.{name}'
       
        return SequenceTask([
            write_information(model_store, lambda ps: ps.create_model(model_id,title)),
            write_information(path_var, lambda pv: pv.write(f'/model/{model_id}'))
        ],progress_check=progress_on_stable)

    return after_dialog('Create model...', enter, validate,
            [('cancel','Cancel','ban',lambda _: constant(None))
            ,('create','Create','plus',save)
            ])


def edit_model(model_id: ModelID, path_var: TaskVariable[str]):
    if model_id is None:
        return constant(None)
    return write_information(path_var, lambda pv:pv.write(f'/model/{model_id}'))

def delete_model(model_store: ModelStore, model_id, path_var: TaskVariable[str], selection_var: TaskVariable[str|None]):
    
    def enter(*args):
        return view_information(f'Are you sure you want to remove "{model_id}"? This cannot be undone.')
    
    def validate(task, action):
        return constant(dict())

    def save(options):
        return sequence_tasks(
            write_information(model_store,lambda ps:ps.delete_model(model_id)),
            write_information(selection_var,lambda sv:sv.write(None)),
            write_information(path_var,lambda pv:pv.write('/model'))
        )
    
    return after_dialog('Remove...',enter,validate,
        [('cancel','No','ban',lambda _: constant(None))
        ,('delete','Yes','trash',save)
        ])


def export_model(model_store: ModelStore, model_id: ModelID):

    def export_docx(model):
        filename = f'{model_id.replace(".","_")}.docx'
        export_headers = [
            (b'Content-Type',b'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
            (b'Content-Disposition',bytes(f'attachment; filename="{filename}"','utf-8'))
        ]
        def view_export(url):
            view = f'''
                <div class="content">
                Download <a href="{url}">{filename}</a>
                </div>
            '''
            return view_information(None,editor=ViewEditor(lambda _: view))
        
        async def export_content():
            return await model_to_docx(model)
        
        return with_download(view_export,export_headers,export_content)

    def export_full_graph_gexf(model):
            filename = f'{model_id.replace(".","_")}.gexf'
            export_headers = [
                (b'Content-Type',b'text/xml'),
                (b'Content-Disposition',bytes(f'attachment; filename="{filename}"','utf-8'))
            ]
            def view_export(url):
                view = f'''
                    <div class="content">
                    Download <a href="{url}">{filename}</a>
                    <div class="content">
                '''
                return view_information(None,editor=ViewEditor(lambda _: view))
            
            async def export_content():
                with tempfile.TemporaryFile() as tmp:
                    nx.write_gexf(nx_full_network(model),tmp)
                    tmp.flush()
                    tmp.seek(0)
                    content = tmp.read()     
                return content
            return with_download(view_export,export_headers,export_content)

    def enter(*args):
        def choose_export():
            options = [
                ('As Microsoft word document','docx'),
                ('As Gephy graph','gefx'),
            ]
            editor = BulmaSelect(options,sync=True)
            return enter_information(editor = editor)

        def view_export(model, selection):
            if selection == 'docx':
                return export_docx(model)
            if selection == 'gefx':
                return export_full_graph_gexf(model)
            return constant(None)
        
        return with_dependent(choose_export(),lambda sel: 
            with_information(model_store,lambda ms:ms.model(model_id),lambda model: view_export(model,sel),refresh=False))

    def validate(task, action):
        return constant(dict())

    return after_dialog('Export...',enter,validate,[('close','Close','ban',lambda _: constant(None))])