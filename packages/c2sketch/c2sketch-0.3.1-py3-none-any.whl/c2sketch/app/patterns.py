from c2sketch.app.ui import TabChoice
from toppyt import (Task, SequenceTask, ParallelTask, TaskResult, TaskStatus, TaskWithDataSource, DataSource, ViewEditor, after_value,
                    all_tasks, constant, end_background, enter_information,
                    progress_on_stable, start_background, update_information,
                    read_information, with_information, with_background_status,
                    with_dependent, view_information, right_task, progress_on_value)
from toppyt.bulma import BulmaButton, BulmaButtons, BulmaButtonSpec
from typing import TypeVar, Callable, Any

def with_source(source, task):
    return TaskWithDataSource(source, lambda _: task)

def action_choice(options, compact_buttons = True):
    buttons = [BulmaButtonSpec(name,label,icon,(task is not None),compact_buttons) for (name,label,icon,task) in options]
    choose = enter_information(editor=BulmaButtons(buttons))
    
    def do_choice(choice):
        for name,_,_,task in options:
            if name == choice:
                return task
        return view_information('')

    return SequenceTask([choose, lambda choice: right_task(choose,do_choice(choice.value))],progress_check=progress_on_value)

def view_with_edit(view_task, edit_task, save_task):
    def progress(step, result):
        if step == 0 and result.value is not None and result.value[1] == 'edit':
            return 1
        elif step == 1 and result.value is not None and result.value[1] == 'cancel':
            return 0
        elif step == 1 and result.value is not None and result.value[1] == 'save':
            return 2
        elif step == 2 and result.status is TaskStatus.STABLE:
            return 0
        return None

    def layout(parts, task_tag):
        return f'<div {task_tag} class="view-with-edit">{parts['buttons']}{parts['task']}</div>'
    
    def result_builder(results):
        return TaskResult([r.value for r in results],TaskStatus.ACTIVE)
    
    view_buttons = [
        BulmaButtonSpec('edit','Edit','edit')
    ]
    edit_buttons = [
        BulmaButtonSpec('cancel','Cancel','cancel',is_escape=True),
        BulmaButtonSpec('save','Save','save',is_enter=True,extra_cls='is-primary')
    ]
    return SequenceTask([
        ParallelTask([
            ('task',view_task),
            ('buttons',enter_information(editor=BulmaButtons(view_buttons)))
        ],layout=layout,result_builder=result_builder),        
        lambda r: ParallelTask([
            ('task',edit_task(r.value[0])),
            ('buttons',enter_information(editor=BulmaButtons(edit_buttons)))
        ],layout=layout, result_builder=result_builder),
        lambda r: save_task(r.value[0])
    ],progress_check= progress)

def choose_task(options,initial):

    edit_options = [(name,name,icon) for (name,icon,_) in options]
    editor = TabChoice(edit_options,compact_tabs=True)
    
    def do_task(choice):
        if choice is None:
            return view_information(None)
        return options[[name for (name,_,_) in options].index(choice)][2]

    def layout(parts,task_tag):
        return f'<div {task_tag} class="choose-task">{parts['task']}{parts['dependency']}</div>'
    
    return ParallelTask(
        [('task',update_information(initial,editor=editor))
        ,('dependency',[('task',initial)],lambda task: do_task(task.value if not task.status is TaskStatus.FAILED else None))
        ], layout=layout)


def configure_and_start(identifier, configure_task, execution_task):
    def control_background(is_running):
        if is_running:
           return after_value(
               enter_information(editor=BulmaButton('Stop')),
               lambda _: end_background(identifier)
            )
        else:
            return after_value(
                all_tasks(
                    configure_task,
                    enter_information(editor=BulmaButton('Start'))
                ),
                lambda config: start_background(execution_task(config[0]),identifier)
            )

    return with_background_status(
        lambda status: with_information(status, lambda s:s.result(identifier),
            lambda background_result:
                control_background(background_result is not None)
        )
    )
