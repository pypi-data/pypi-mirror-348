import asyncio, aiofiles
import os
import tempfile
import pygraphviz as pgv

from toppyt import (ParallelTask, ViewEditor, after_value,
                    all_tasks, any_task, enter_information, fail,
                    forever, map_value, constant,
                    update_information, view_information, with_information,
                    with_dependent, with_download, write_information)
from toppyt.bulma import (BulmaRecordEditor, BulmaSelect, BulmaTextArea,
                          BulmaTextInput)

from c2sketch.models import name_from_model_id, ModelSet

from ...patterns import choose_task, view_with_edit
from ...ui import ConfirmedDropdown, TableChoice, SourceView, SourceEditor, SVGCanvas, view_title
from ....visualizations import svg_org_chart, svg_task_hierarchy, dot_actor_information_flow
from ...data import ModelStore
from ...config import AppConfig

__all__ = ('edit_model_node',)

def edit_model_node(model_store, model_id, path_var):
    
    def layout(parts,task_tag):
        return f'<div {task_tag} class="node-edit">{parts['title']}{parts['main']}</div>'
   
    return ParallelTask([
        ('title',view_title(name_from_model_id(model_id))),
        ('main',choose_task([
            ('Attributes','file-alt', edit_attributes(model_store, model_id)),
            ('Task decomposition', 'sitemap', view_task_decomposition(model_store,model_id)),
            ('Organization chart','users-rectangle',view_organization_chart(model_store,model_id)),
            ('Information flow','code-compare',view_information_flow(model_store,model_id)),
            ('Imports','arrow-down',edit_imports(model_store, model_id)),
            ('Source','code', view_model_source(model_store,model_id))
        ],'Attributes'))
    ],layout=layout)
    
def edit_attributes(planstore: ModelStore, plan_id):
    def view():
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title',disabled = True)),
            ('summary',BulmaTextArea(label= 'Summary', disabled = True))
        ])
        return view_information(planstore,lambda ps: ps.model_attributes(plan_id), editor=editor)
    
    def edit(fields):
        editor = BulmaRecordEditor([
            ('name',BulmaTextInput(label = 'Name', disabled = True)),
            ('title',BulmaTextInput(label = 'Title')),
            ('summary',BulmaTextArea(label= 'Summary'))
        ])
        return update_information(fields, editor=editor)
    
    def save(updated_fields):
        return write_information(planstore,lambda ps:ps.write_model_attributes(plan_id, updated_fields))

    return view_with_edit(view(),edit,save)

def edit_imports(model_store: ModelStore, model_id):
    def choose_action():
        def choose(imports,import_options):
            choice_options = [(iname,[iname],[('delete','Delete','trash')]) for iname in imports]
            add_options = sorted(n for (n,_,_) in import_options if n not in imports)
            return any_task(
                enter_information(editor=TableChoice(choice_options)),
                map_value(enter_information(editor=ConfirmedDropdown(add_options,'Add import',icon='plus')),lambda c: (c,'add'))
            )

        return with_information(model_store,lambda ps:ps.model_imports(model_id), lambda a:
            with_information(model_store,lambda ps:ps.list_models(), lambda ao: choose(a,ao)))

    def do_action(subject,action):
            if action == 'add':
                return write_information(model_store,lambda ps:ps.model_add_import(model_id,subject))
            elif action == 'delete':
                return write_information(model_store,lambda ps:ps.model_remove_import(model_id,subject))
            return fail('Unknown action')

    return forever([after_value(choose_action(),lambda r: do_action(*r))])

def view_task_decomposition(model_store: ModelStore, model_id):
 
    def view(model_set: ModelSet):
       
        return view_information(svg_task_hierarchy(model_set, model_id),editor=SVGCanvas())
    
    return with_information(model_store,lambda ms: ms.model_complete(model_id),view)
    
   
def view_organization_chart(model_store: ModelStore, model_id):

    def view(model_set: ModelSet):
        return view_information(svg_org_chart(model_set, model_id),editor=SVGCanvas())
    
    return with_information(model_store,lambda ms: ms.model_complete(model_id),view)

def view_information_flow(model_store: ModelStore, model_id):

    def view_graph(url):
        return view_information(url,editor=ViewEditor(lambda u: f'<img src="{u}" alt="Information flow graph">'))
    
    async def generate_graph():
        op_flow_dot = dot_actor_information_flow(model_store.model_set, model_id)
        with tempfile.TemporaryDirectory() as workdir:
            dotfile_path =os.path.join(workdir,'op-flow.dot')
            pngfile_path =os.path.join(workdir,'op-flow.png')
            async with aiofiles.open(dotfile_path, mode='w') as f:
                await f.write(op_flow_dot)

            dot_graph = pgv.agraph.AGraph()
            dot_graph.read(dotfile_path)
            dot_graph.draw(pngfile_path, prog='dot')
            
            #Async version which requires explicit executable path instead of pygraphviz
            #dot = await asyncio.create_subprocess_exec('/opt/homebrew/bin/dot','-Tpng',dotfile_path,'-o',pngfile_path)
            #await dot.wait()
            
            async with aiofiles.open(pngfile_path, mode='rb') as f:
                png_data = await f.read()
            return png_data

    return with_download(view_graph,[(b'Content-Type',b'image/png')],generate_graph)

def view_model_source(model_store: ModelStore, model_id):

    def view():
        return with_information(model_store,lambda ms: ms.model_problems(model_id), lambda problems:                     
                view_information(model_store,lambda ms: ms.model_source(model_id),editor=SourceView(problems)))
    
    def edit(value):
        return update_information(value,editor=SourceEditor())
    
    def save(value):
        return write_information(model_store,lambda ms: ms.write_model_source(model_id,value))
        
    return view_with_edit(view(),edit,save)