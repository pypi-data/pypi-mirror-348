


from toppyt import (Editor, MappedEditor, ParallelTask, TaskResult, TaskStatus,
                    ViewEditor, TaskVariable, after_task, constant, update_information,
                    enter_information, view_information, map_value) 
from toppyt.bulma import (BulmaButtons, BulmaFloatInput, BulmaIntInput,
                          BulmaCheckboxField, BulmaInputBase,
                          BulmaRecordEditor, BulmaSelect, BulmaTextArea,
                          BulmaTextInput, BulmaTextView, BulmaButtonSpec
                          )
from dataclasses import dataclass
from c2sketch import models
from typing import Iterable, Any
from html import escape

#Util
def path_level(depth,path):
    if path is None:
        return None
    parts = path[1:].split("/")
    return None if depth > len(parts) -1 or parts[depth] == '' else parts[depth]

def path_levels(depth,path):
    if path is None:
        return None
    parts = path[1:].split("/")
    return None if depth > len(parts) -1 else parts[depth:]


# Shared layout
def model_header(title = '', actor_title = '', actor_location ='', execution_time='', app_mode=''):
    return f'''
        <div class="is-small">
            <div class="navbar">
                <div class="navbar-brand">
                    <div class="navbar-item"><img src="/static/c2s-logo.png" alt="{title}"></div>
                </div>
                <div class="navbar-start">
                    <div class="navbar-item">{actor_title}</div>
                    <div class="navbar-item">{actor_location}</div>
                    <div class="navbar-item">{execution_time}</div>
                </div>
                <div class="navbar-end">
                    <div class="navbar-item">
                    {app_mode}
                    </div>
                </div>
            </div>
        </div>
    '''

def execute_header(actor_choice = '', actor_location ='', scenario_time = '', scenario_control='', app_mode=''):
    return f'''
        <div class="is-small">
            <div class="navbar">
                <div class="navbar-brand">
                    <div class="navbar-item"><img src="/static/c2s-logo.png"></div>
                </div>
                <div class="navbar-start">
                    <div class="navbar-item">{actor_choice}</div>
                    <div class="navbar-item">{actor_location}</div>
                </div>
                <div class="navbar-end">
                    <div class="navbar-item">{scenario_time}</div>
                    <div class="navbar-item">{scenario_control}</div>
                    <div class="navbar-item">{app_mode}</div>
                </div>
            </div>
        </div>
    '''

# Common tasks
def view_model_title(model_id: models.ModelID | None, model_title: str | None, path_var):
    
    if model_id is None:
        return constant(None)

    value = f'/model/{model_id}'
    title = model_id if model_title is None else f'{model_title} ({model_id})'

    return update_information(path_var,editor=SubTitleLink(value,title))

def choose_app_mode(path_var):
    options = [
        (f'/model','Model','edit'),
        (f'/execute','Execute','play')
    ]
    
    async def read_fun(pv: TaskVariable[str]):
        path = await pv.read()
        return "/".join(path.split("/")[:2])
    return update_information(path_var, read_fun, lambda pv, u: pv.write(u), editor=BulmaButtons(options))
                             

# Convenient tasks

def map_ui(layout_fun, task):
    return ParallelTask([('task',task)], layout = lambda parts: layout_fun(parts['task']))

def view_title(title):
    return view_information(title,editor=ViewEditor(lambda t: f'<h1 class="title mb-2">{t}</h1>\n'))

def with_actions(actions,task):
    def has_action(results):
        if results[1].value is None:
            return TaskResult(None,TaskStatus.ACTIVE)
        else:
            return TaskResult([results[0].value,results[1].value],TaskStatus.ACTIVE)
    return ParallelTask([
        task,
        enter_information(editor=BulmaButtons(actions))
    ],result_builder=has_action) 

def after_dialog(title, enter_task, validate_task, continuations):
    def do_choice(choice):
        for name,_,_,task in continuations:
            if name == choice[1]:
                return task(choice[0])
        return constant(None)
    
    def result(results):
        if results[1].status is TaskStatus.FAILED:
            return results[1]
        if results[2].value is not None and results[3].value is not None and len(results[3].value) == 0:
            return TaskResult((results[1].value,results[2].value),TaskStatus.STABLE)
        
        return TaskResult(None,TaskStatus.ACTIVE)
    
    def enter_actions(action,validate):
        editor = BulmaButtons([(name,label,icon) for (name,label,icon,_) in continuations])
        value = None if validate is not None and len(validate) > 0 else action

        return update_information(value, editor=editor)
    
    def validate_dialog(validate,task,action):
        if validate is None and action is None:
            return constant(None)

        return validate_task(task,action)

    return after_task(ParallelTask([
        ('title', view_information(title)),
        ('task', ['task','validate'], lambda task, validate: enter_task(task.value, validate.value)),
        ('action', ['action','validate'], lambda action, validate: enter_actions(action.value, validate.value)),
        ('validate', ['validate','task','action'], lambda validate, task, action: validate_dialog(validate.value,task.value,action.value)),
        ],layout=bulma_modal_dialog_layout,result_builder=result),do_choice)

def with_action_check(action,task):
    def check(errors):
        if action is not None and len(errors) > 0:
            errors['action'] = 'not yet valid'
        return errors
    return map_value(task,check)

def bulma_modal_dialog_layout(parts, task_tag):
    return f'''
    <div {task_tag} class="modal is-active">
    <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">{parts['title']}</p>
            </header>
            <section class="modal-card-body">
            {parts['task']}
            </section>
            <footer class="modal-card-foot">
            {parts['action']}
            </footer>
        </div>
    </div>
    '''

def inline_dialog(enter_task, validate_task, continuations):
    def do_choice(choice):
        for name,_,_,task in continuations:
            if name == choice[1]:
                return task(choice[0])
        return constant(None)

    def result(results):
        if results[0].status is TaskStatus.FAILED:
            return results[1]
        if results[1].value is not None and results[2].value is not None and len(results[2].value) == 0:
            return TaskResult((results[0].value,results[1].value),TaskStatus.STABLE)
        
        return TaskResult(None,TaskStatus.ACTIVE)

    def enter_actions(action,validate):
        editor = BulmaButtons([(name,label,icon) for (name,label,icon,_) in continuations])
        value = None if validate is not None and len(validate) > 0 else action

        return update_information(value, editor=editor)

    def validate_dialog(validate,task,action):
        if validate is None and action is None:
            return constant(None)

        return validate_task(task,action)

    return after_task(ParallelTask([
        ('task', ['task','validate'], lambda task, validate: enter_task(task.value, validate.value)),
        ('action', ['action','validate'], lambda action, validate: enter_actions(action.value, validate.value)),
        ('validate', ['validate','task','action'], lambda validate, task, action: validate_dialog(validate.value,task.value,action.value)),
        ],result_builder=result),do_choice)


# Custom editors
def record_editor(record_type: models.RecordType, label = None, disabled: bool = False) -> Editor:
    parts: list[tuple[str,Editor]] = list()
    for field in record_type.fields:
        if field.type == 'string' or field.type == 'str':
            #if field.choices is not None:
            #    parts.append((field.name,BulmaSelect(field.choices,label=field.name,disabled=disabled)))
            #else:
            parts.append((field.name,BulmaTextInput(label=field.name,disabled=disabled)))
        elif field.type == 'text':
            parts.append((field.name,BulmaTextArea(label=field.name,disabled=disabled)))
        elif field.type == 'integer' or field.type == 'int':
            parts.append((field.name,BulmaIntInput(label=field.name,disabled=disabled)))
            # parts.append((field.name, MappedEditor(
            #     BulmaIntInput(label=field.name,disabled=disabled),
            #     models.PrimitiveType.INTEGER_TYPE.from_string,
            #     models.PrimitiveType.INTEGER_TYPE.to_string)
            # ))
        # elif field.type is models.PrimitiveType.INTEGER2_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaTupleEditor([BulmaIntInput(disabled=disabled),BulmaIntInput(disabled=disabled)],label=field.name),
        #         models.PrimitiveType.INTEGER2_TYPE.from_string,
        #         models.PrimitiveType.INTEGER2_TYPE.to_string)
        #     ))
        # elif field.type is models.PrimitiveType.INTEGER3_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaTupleEditor([BulmaIntInput(disabled=disabled),BulmaIntInput(disabled=disabled),BulmaIntInput(disabled=disabled)],label=field.name),
        #         models.PrimitiveType.INTEGER3_TYPE.from_string,
        #         models.PrimitiveType.INTEGER3_TYPE.to_string)
        #     ))
        # elif field.type is models.PrimitiveType.REAL_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaFloatInput(label=field.name,disabled=disabled),
        #         models.PrimitiveType.REAL_TYPE.from_string,
        #         models.PrimitiveType.REAL_TYPE.to_string)
        #     ))
        # elif field.type is models.PrimitiveType.REAL2_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaTupleEditor([BulmaFloatInput(disabled=disabled),BulmaFloatInput(disabled=disabled)],label=field.name),
        #         models.PrimitiveType.REAL2_TYPE.from_string,
        #         models.PrimitiveType.REAL2_TYPE.to_string)
        #     ))
        # elif field.type is models.PrimitiveType.REAL3_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaTupleEditor([BulmaFloatInput(disabled=disabled),BulmaFloatInput(disabled=disabled),BulmaFloatInput(disabled=disabled)],label=field.name),
        #         models.PrimitiveType.REAL3_TYPE.from_string,
        #         models.PrimitiveType.REAL3_TYPE.to_string)
        #     ))  
        # elif field.type is models.PrimitiveType.BOOLEAN_TYPE:
        #     options = [('True','true'),('False','false')]
        #     parts.append((field.name,BulmaSelect(options,label=field.name,disabled=disabled)))
        # elif field.type is models.PrimitiveType.TIMESTAMP_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaIntInput(label=field.name,disabled=disabled),
        #         models.PrimitiveType.INTEGER_TYPE.from_string,
        #         models.PrimitiveType.INTEGER_TYPE.to_string)
        #     ))
        # elif field.type is models.PrimitiveType.LATLNG_TYPE:
        #     parts.append((field.name, MappedEditor(
        #         BulmaTupleEditor([BulmaFloatInput(disabled=disabled),BulmaFloatInput(disabled=disabled)],label=field.name),
        #         models.PrimitiveType.LATLNG_TYPE.from_string,
        #         models.PrimitiveType.LATLNG_TYPE.to_string)
        #     ))
        # 
    return BulmaRecordEditor(parts, label = label)

def record_view(message_type: models.RecordType) -> Editor:
    parts = list()
    for field in message_type.fields:
        parts.append((field.name,BulmaTextView(label=field.name)))
    return BulmaRecordEditor(parts)

def untyped_record_editor(label: str | None = None) -> Editor:
    #TODO make a specialized editor which allows adding arbitrary record fields
    return BulmaRecordEditor([
        ("data",BulmaTextArea(label="Data"))
    ],label=label)

class BulmaStrDictEditor(Editor[dict[str,str]]):
    parts: list[tuple[Editor[str],Editor[str]]]
    label: str | None

    def __init__(self, label: str | None = None):
        self.label = label
        self.parts = []
    
    def start(self, value: dict[str,str] | None) -> None:
        if value is not None:
            for key, value in value.items():
                key_part = BulmaTextInput()
                key_part.start(key)
                value_part = BulmaTextInput()
                value_part.start(value)
                self.parts.append((key_part,value_part))

    def generate_ui(self, name: str = 'v', task_tag: str = '') -> str:
        parts_html = []

        for i, (key_part,value_part) in enumerate(self.parts):
            parts_html.append(key_part.generate_ui(f'{name}-key_{i}'))
            parts_html.append(value_part.generate_ui(f'{name}-value_{i}'))

        if self.label is None:
            return "".join(parts_html)

        return f'''
            <div {task_tag} class="message mt-2">
            <div class="message-header">{self.label}</div>
            <div class="message-body">{"".join(parts_html)}</div>
            </div>
            '''

    def handle_edit(self, edit: Any) -> bool:
        update = False
        for i, (key_part, value_part) in enumerate(self.parts):
            if f'key_{i}' in edit:
                update = update or key_part.handle_edit(edit[f'key_{i}'])
            if f'value_{i}' in edit:
                update = update or value_part.handle_edit(edit[f'value_{i}'])
        return update

    def get_value(self) -> dict[str,Any]:
        value = {}
        for (key_part, value_part) in self.parts:
            key = key_part.get_value()
            if key is not None and key != '':
                value[key] = value_part.get_value()
        return value

def compact_message(message):
    if message is None:
        return '-'
    return ', '.join(f'{k}: {v}' for k,v in message.items())

class SubTitleLink(Editor):
    def __init__(self, value, title):
        self.value = value
        self.title = title
    def generate_ui(self, name='v', task_tag = ''):
        return f'<a {task_tag} href="#" class="navbar-item" onclick="toppyt_notify(this,true,\'{name}\',\'{self.value}\');return false;"><h2 class="subtitle">{self.title}</h2></a>'
 
    def handle_edit(self, edit) -> bool:
        return super().handle_edit(edit)
        
    def get_value(self):
        return self.value

class NavBarChoice(Editor):
    def __init__(self,options):
        self.options = options

    def start(self, value: str | None) -> None:
        self._raw = value
        
    def generate_ui(self, name='v'):
        return ''.join([self.option_html(name, value, label, icon) for value, label, icon in self.options])

    def option_html(self,name,value,label,icon):
        return f'<a href="#" class="navbar-item" onclick="toppyt_notify(this,true,\'{name}\',\'{value}\');return false;"><span class="icon"><i class="fas fa-{icon}"></i></span><span>{label}</span></a>'
 
    def handle_edit(self, edit) -> bool:
        return super().handle_edit(edit)
        
    def get_value(self):
        return self._raw

class TreeChoice(Editor):
    def __init__(self,options):
        self.options = options
    
    def start(self, value):
        self._raw = value
        
    def generate_ui(self, name='v', task_tag = ''):
        def to_html(options):
            lis = list()
            for option in options:
                children_html = to_html(option['children']) if 'children' in option else '' 
                
                selected = ' class="selected" ' if (option['value'] is not None and self._raw == option['value']) else ''
                value = option["value"] if option["value"] is not None else ''
                lis.append(f'<li {selected}><span class="icon"><i class="fas fa-{option["icon"]}"></i></span><a href="#" onclick="toppyt_notify(this,true,\'{name}\',\'{value}\');return false;">{option["name"]}</a>{children_html}</li>')
            return '<ul>'+''.join(lis)+'</ul>'

        return f'<div {task_tag} class="treeview">{to_html(self.options)}</ul></div>'
    
    def handle_edit(self, edit) -> bool:
        self._raw = edit
        return True
        
    def get_value(self):
        return self._raw

class TabChoice(Editor):
    compact_tabs: bool

    def __init__(self,options,compact_tabs = False):
        self.options = options
        self.compact_tabs = compact_tabs

    def start(self, value):
        self._raw = value

    def generate_ui(self,name='v', task_tag=''):
        options = ''.join([self.option_html(*option) for option in self.options])
        return f'<div {task_tag} class="tabs is-boxed mb-2"><ul>{options}</ul></div>'
    
    def option_html(self,value,label,icon):
        is_active = value == self._raw
        active_html = 'class="is-active"' if is_active else ''
        label_html = '' if self.compact_tabs and not is_active else f'<span>{label}</span>'
        
        return f'<li {active_html}><a href="#" title="{label}" onclick="toppyt_notify(this,true,\'v\',\'{value}\');return false;"><span class="icon"><i class="fas fa-{icon}"></i></span>{label_html}</a></li>'

    def handle_edit(self, edit) -> bool:
        self._raw = edit
        return True
        
    def get_value(self):
        return self._raw
        
class MenuChoice(Editor):
    def __init__(self,options,label=None):
        self.options = options
        self.label = label
    
    def generate_ui(self,name='v', task_tag = ''):
        label_html = '' if self.label is None else f'<p class="menu-label">{self.label}</p>' 
        options_html = ''.join([self.option_html(name,v,l) for (v,l) in self.options])
        return f'<div {task_tag} class="menu">{label_html}<ul class="menu-list">{options_html}</ul></div>'

    def option_html(self,name,value,label):
        active = 'class="is-active"' if (value == self._raw) else ''
        return f'<li><a href="#" {active} onclick="toppyt_notify(this,true,\'{name}\',\'{value}\');return false;">{label}</a></li>'

class BreadcrumbChoice(Editor):
    def __init__(self,options):
        self.options = options
    
    def start(self, value: Any | None) -> None:
        self.value = value
    
    def generate_ui(self,name='v', task_tag=''):
        options_html = ''.join([self.option_html(name,v,l) for (l,v) in self.options])
        return f'<div {task_tag} class="breadcrumb"><ul>{options_html}</ul></div>'

    def option_html(self,name,value,label):
        active = 'class="is-active"' if (value == self.value) else ''
        return f'<li><a href="#" {active} onclick="toppyt_notify(this,true,\'{name}\',\'{value}\');return false;">{label}</a></li>'

    def handle_edit(self, edit) -> bool:
        self.value = edit
        return True

    def get_value(self):
        return self.value if isinstance(self.value,str) else None


def CheckboxChoice(options: list[str | tuple[str,str]],label=None,disabled=False):

    expanded_options = [(opt,opt) if isinstance(opt,str) else opt for opt in options]
    
    parts = [(name.replace('-','_'), BulmaCheckboxField(label,disabled=disabled,sync=True)) for name, label in expanded_options]
    editor = BulmaRecordEditor(parts,label=label)
    
    def start_map(selection):
        if selection is None:
            selection = []
        checks = {}
        for name, _ in expanded_options:
            checks[name.replace('-','_')] = name in selection
        return checks
    def value_map(checks):
        selection = []
        for name, value in expanded_options:
            if checks[name.replace('-','_')]:
                selection.append(value)
        return selection
    return MappedEditor(editor,start_map=start_map,value_map=value_map)
    

##TODO Implement customized CheckboxChoice with actual checking/unchecking
# @dataclass
# class CheckboxChoice(BulmaInputBase[str]):
#     options: list[str | tuple[str,str]]
#     label: Optional[str]
#     placeholder: Optional[str]
#     text: Optional[str]
#     icon: Optional[str]
#     help: Optional[str | tuple[str,str]]
#     disabled: bool
#     sync: bool
    
#     _raw: list[str] = field(default_factory=list)

#     def __init__(self,
#         options: Iterable[str | tuple[str,str]],
#         label:Optional[str] = None,
#         placeholder: Optional[str] = None,
#         icon: Optional[str] = None,
#         help: Optional[str | tuple[str,str]] = None,
#         disabled: bool = False,
#         sync: bool = False):
        
#         self.options = list(options)
#         self.label = label
#         self.placeholder = placeholder
#         self.icon = icon
#         self.help = help
#         self.disabled = disabled
#         self.sync = sync

#     def start(self, value) -> None:
#         self._raw = value

#     def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
#         parts = []
        
#         options = [v if isinstance(v,tuple) else (v,v) for v in self.options]
#         for k, v in options:
#             checked = 'checked' if v in self._raw else ''

#             parts.append(self.option_html(v,k,checked,disabled_attr))
#         options_html = '<br>'.join(parts)

#         return f'<div class="field is-fullwidth{help_class}">{options_html}</div>'

#     def option_html(self,value,label,checked,disabled_attr):
#         return f'<label class="checkbox"><input type="checkbox" {checked} {disabled_attr}> {label}</label>'
 
#     def get_value(self):
#         return self._raw if isinstance(self._raw,list) else []
    
class PlanChoice(Editor[str]):
    def __init__(self,options):
        self.options = options

    def generate_ui(self,name='v'):
        return ''.join([self.option_html(name,*option) for option in self.options])

    def option_html(self,name,value,title,summary,actions):
        action_html = ''.join([self.action_html(*action) for action in actions])
        def html(s):
            return escape(s).replace("\n","<br/>")
        return f'''
        <div class="box">
            <div class="block">
            <h1 class="title"><a onclick="toppyt_notify(this,true,'{name}','{value}')">{html(title)}</a></h1>
            <p>{html(summary)}</p>
            </div>
            <div class="buttons is-right">
            {action_html}
            </div>     
        </div>'''

    def action_html(self,value,label,icon):
        return f'<button class="button is-primary has-icon" name="v" value="{value}" onclick="toppyt_notify(this,true)"><span class="icon"><i class="fas fa-{icon}"></i></span><span>{label}</span></button>'

    def handle_edit(self, edit) -> bool:
        self._raw = edit
        return True

    def get_value(self):
        return self._raw if isinstance(self._raw,str) else None

class TaskTriggerChoice(Editor[str]):
    def __init__(self,options, label = None):
        self.options = options
        self.label = label

    def generate_ui(self,name='v'):
        control_html = ''.join([self.option_html(name,v,t,s) for (v,t,s) in self.options])
        if self.label is None:
            return control_html
        else:
            return f'''
            <div class="field">
                <label class="label">{self.label}</label>
                {control_html}
            </div>
            '''

    def option_html(self,name,value,title,summary):
        checked = 'checked' if value == self._raw else ''
        return f'''
        <div class="control">
            <label class="radio">
            <input type="radio" name="{name}" {checked} onclick="toppyt_notify(this,true,'{name}','{value}')">
             <strong>{title}</strong><br>
            {summary}
            </label>
        </div>
        '''

    def handle_edit(self, edit) -> bool:
        self._raw = edit
        return True
        
    def get_value(self):
        return self._raw if isinstance(self._raw,str) else None

class TableChoice(Editor):
    def __init__(self,options, headers = None, compact_buttons = True):
        self.options = options
        self.headers = headers
        self.compact_buttons = compact_buttons

    def start(self, value) -> None:
        self._raw = None

    def generate_ui(self,name='v',task_tag=''):
        options = ''.join([self.option_html(*option) for option in self.options])
        header = ''
        has_actions = any(len(option[2]) > 0 for option in self.options)
        if self.headers is not None:
            row = ''.join([f'<th>{header}</th>' for header in self.headers])
            header = f'<tr>{row}{"<th>&nbsp;</th>" if has_actions else ""}</tr>' #Extra column for actions
        return f'<div {task_tag} class="field"><table class="table is-fullwidth is-striped">{header}{options}</table></div>'
    
    def option_html(self, value, columns, actions):
        columns_html = [self.column_html(value,col) for col in columns]
        if len(actions) > 0:
            actions_html = [self.action_html(value,action,label,icon) for (action,label,icon) in actions]
            columns_html.append(f'<td class="has-text-right">{"".join(actions_html)}</td>')
    
        return f'<tr>{"".join(columns_html)}</tr>'

    def column_html(self,value,col):
        if isinstance(col,tuple):
            return f'<td><a href="#" onclick="toppyt_notify(this,true,\'v\',\'{value}:{col[0]}\');return false;">{col[1]}</a></td>'
        else:
            return f'<td>{col}</td>'

    def action_html(self,value,action,label,icon):
        csscls = 'button has-icon'
        if action == 'delete':
            csscls += ' is-danger'
        if self.compact_buttons:
            label_html = ''
        else:
            label_html = f'<span>{label}</span>'

        return f'<button class="{csscls}" title="{label}" name="v" value="{value}:{action}" onclick="toppyt_notify(this,true)"><span class="icon"><i class="fas fa-{icon}"></i></span>{label_html}</button>'

    def get_value(self):
        return tuple(self._raw.split(":")) if self._raw is not None else None

    def handle_edit(self,edit):
        self._raw = edit
        return True

class TableSelect(Editor[list[str | None]]):

    def __init__(self, rows: list[list[str]], headers: list[str], options: Iterable[str | tuple[str, str]] | None = None):
        self.rows = rows
        self.headers = headers
        self.editors = [BulmaSelect(options) for _ in range(len(rows))]

    def start(self, value):
        self.selection = value
        for editor, editor_value in zip(self.editors,value):
            editor.start(editor_value)
    
    def generate_ui(self,name='v'):
        options = ''.join([self.row_html(name, i, row) for i, row in enumerate(self.rows)])
        header = ''
        if self.headers is not None:
            header = ''.join([f'<th>{header}</th>' for header in self.headers])
        return f'<div class="field"><table class="table is-fullwidth is-striped">{header}{options}</table></div>'
    
    def row_html(self, name, i, columns):
        columns_html = [ f'<td>{col}</td>' for col in columns]
        
        #Column for editor
        inner_ui = self.editors[i].generate_ui(f'{name}-{i}')
        columns_html.append(f'<td class="has-text-right">{inner_ui}</td>')
    
        return f'<tr>{"".join(columns_html)}</tr>'

    def get_value(self):
        return [editor.get_value() for editor in self.editors]
     
    def handle_edit(self,edit):
        if isinstance(edit,dict):
            for key, value in edit.items():
                self.editors[int(key)].handle_edit(value)
            return True
        return False
    
class ConfirmedDropdown(Editor):
    def __init__(self, options, label, icon = None):
        self.options = options
        self.label = label
        self.icon = icon

    def start(self, value):
        self._raw = value

    def generate_ui(self, name = 'v', task_tag=''):
        parts = []
        options = [v if isinstance(v,tuple) else (v,v) for v in self.options]
        for value, label in [('',"Select...")] + options:
            selected = 'selected' if value == self._raw else ''
            parts.append(f'<option value="{value}" {selected}>{label}</option>')

        options_html = ''.join(parts)

        select_html = f'<p class="control"><span class="select"><select name="{name}-select" onchange="toppyt_notify(this,false)">{options_html}</select></span></p>'
        button_html = f'<p class="control"><button class="button is-info has-icon" name="{name}-confirm" value="confirm" onclick="toppyt_notify(this,true)"><span class="icon"><i class="fas fa-{self.icon}"></i></span><span>{self.label}</span></button></p>'
        return f'<div {task_tag} class="field has-addons has-addons-right">{select_html}{button_html}</div>'

    def handle_edit(self, edit) -> bool:
        self._raw = edit
        return True
        
    def get_value(self):
        if self._raw == '' or self._raw is None:
            return None

        if 'select' in self._raw:
            return self._raw['select']

        return None

class LatLngField(Editor):
    _raw_lat: str = ''
    _raw_lng: str = ''

    def __init__(self, label = None):
        self.label = label

    def begin(self,value):
        if value is None:
            self._raw_lat = ''
            self._raw_lng = ''
        else:
            self._raw_lat = str(value[0])
            self._raw_lng = str(value[1])
        
    def generate_ui(self, name='v'):
        control_html = f'''
        <div class="field has-addons">  
        <div class="control">
            <input class="input" name="{name}-lat" placeholder="Lattitude" size="5" value="{self._raw_lat}" />
        </div>
        <div class="control"><button class="button is-static">&deg;N</button></div>
        <div class="control">
            <input class="input" name="{name}-lng" placeholder="Longitude" size="5" value="{self._raw_lng}"/>
        </div>
        <div class="control"><button class="button is-static">&deg;E</button></div>
        </div>
        '''
        if self.label is None:
            return control_html
        else:
            return f'''
            <div class="field">
                <label class="label">{self.label}</label>
                {control_html}
            </div>
            '''

    def handle_edit(self,edit):
        if 'lat' in edit:
            self._raw_lat = edit['lat']
        if 'lng' in edit:
            self._raw_lng = edit['lng']

    def get_value(self):
        if self._raw_lat.isnumeric() and self._raw_lng.isnumeric():
            return (float(self._raw_lat),float(self._raw_lng))
        return None

class SourceView(Editor):
    
    def __init__(self, problems: list[tuple[int,int,str]] | None = None):
        self.problems = []if problems is None else problems
        super().__init__()

    def start(self,value):
        self.value = value
    
    def generate_ui(self, name='v', task_tag=''):
        problems_html = ''.join(f'<c2s-problem start="{start}" end="{end}">{escape(problem)}</c2s-problem>' for start, end, problem in self.problems)

        return f'<c2s-editor {task_tag} enabled="false"><c2s-code>{escape(self.value)}</c2s-code>{problems_html}</c2s-editor>'
    
    def get_value(self):
        return self.value

class SourceEditor(Editor):
    def start(self,value):
        self.value = value
    
    def generate_ui(self, name='v', task_tag = ''):
        return f'<c2s-editor {task_tag} name="{name}" onchange="toppyt_notify(this,false)"><c2s-code>{escape(self.value)}</c2s-code></c2s-editor>'
    
    def handle_edit(self, edit) -> bool:
        self.value = edit
        return False #Don't refresh UI
    
    def get_value(self):
        return self.value

class SVGCanvas(Editor[str]):
    def __init__(self):
        super().__init__()
        
    def start(self, value: str | None):
        self.value = value

    def generate_ui(self, name: str, task_tag: str) -> str:
        return f'<svg-canvas {task_tag}>{self.value}</svg-canvas>'

    def get_value(self) -> str | None:
        return self.value
    
@dataclass
class ButtonsRowSpec:
    buttons: list[BulmaButtonSpec]

class BulmaButtonsTable(Editor[str]):
    def __init__(self,options, headers = None, compact_buttons = True):
        self.options = options
        self.headers = headers
        self.compact_buttons = compact_buttons

    def start(self, value) -> None:
        self.value = None

    def generate_ui(self,name='v'):
        options = ''.join([self.option_html(*option) for option in self.options])
        header = ''
        has_actions = any(len(option[2]) > 0 for option in self.options)
        if self.headers is not None:
            row = ''.join([f'<th>{header}</th>' for header in self.headers])
            header = f'<tr>{row}{"<th>&nbsp;</th>" if has_actions else ""}</tr>' #Extra column for actions
        return f'<div class="field"><table class="table is-fullwidth is-striped">{header}{options}</table></div>'
    
    def option_html(self, value, columns, actions):
        columns_html = [self.column_html(value,col) for col in columns]
        if len(actions) > 0:
            actions_html = [self.action_html(value,action,label,icon) for (action,label,icon) in actions]
            columns_html.append(f'<td class="has-text-right">{"".join(actions_html)}</td>')
    
        return f'<tr>{"".join(columns_html)}</tr>'

    def column_html(self,value,col):
        if isinstance(col,tuple):
            return f'<td><a href="#" onclick="toppyt_notify(this,true,\'v\',\'{value}:{col[0]}\');return false;">{col[1]}</a></td>'
        else:
            return f'<td>{col}</td>'

    def action_html(self,value,action,label,icon):
        csscls = 'button has-icon'
        if action == 'delete':
            csscls += ' is-danger'
        if self.compact_buttons:
            label_html = ''
        else:
            label_html = f'<span>{label}</span>'

        return f'<button class="{csscls}" title="{label}" name="v" value="{value}:{action}" onclick="toppyt_notify(this,true)"><span class="icon"><i class="fas fa-{icon}"></i></span>{label_html}</button>'

    def get_value(self):
        return tuple(self.value.split(":")) if self.value is not None else None

    def handle_edit(self,edit):
        if isinstance(edit,str):
            self.value = edit
        return True


class BulmaToggleField(BulmaInputBase[bool]):
    label: str | None
    placeholder: str | None
    text: str | None
    icon: str | None
    help: str | tuple[str,str] | None
    disabled: bool
    sync: bool

    _checked: bool = False
    
    def __init__(self,
        label: str | None = None,
        placeholder: str | None = None,
        text: str | None = None,
        icon: str | None = None,
        help: str | tuple[str,str] | None = None,
        disabled: bool = False,
        sync: bool = False):
        
        self.label = label
        self.placeholder = placeholder
        self.text = text
        self.icon = icon
        self.help = help
        self.disabled = disabled
        self.sync = sync

    def start(self, value: Any) -> None:
        self._checked = value if isinstance(value,bool) else False

    def _generate_input(self, name: str, help_class: str, placeholder_attr: str, sync_attr: str, disabled_attr: str) -> str:
        checked_attr = 'checked' if self._checked else ''
        text_attr = '' if self.text is None else escape(self.text)
        return f'<label class="toggle{help_class}"><input type="checkbox" name="{name}" {checked_attr} oninput="toppyt_notify(this,{sync_attr});" {disabled_attr}><div class="switch"></div><span>{text_attr}</span></label>'

    def handle_edit(self, edit: Any) -> bool:
        self._checked = edit
        return True

    def get_value(self) -> bool:
        return self._checked