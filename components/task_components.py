from fasthtml import common as c
from components.search_component import AutoSearch

class Pages:
    @staticmethod
    def dashboard_page(message=None, message_type=None):
        return c.Titled('Dashboard',
                     c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P()),
                        c.P('Welcome to your dashboard!'),
                        c.Div(c.Form(c.Button('Logout', type='submit'), method='POST', action='/logout')),
                        c.Div(c.Form(c.Button('CREATE TASK', type = "submit"), method='GET', action='/create_task')),
                        c.Div(c.Form(c.Button('VIEW TASKS', type = "submit"), method='GET', action='/view_tasks')),
                        c.Div(c.Form(c.Button('UPDATE TASKS', type = "submit"), method='GET', action='/search-update-tasks')),
                        c.Div(c.Form(c.Button('DELETE TASKS', type = "submit"), method='GET', action='/delete-tasks')),
                        c.Div(c.Form(c.Button('COMPLETE TASKS', type = "submit"), method='GET', action='/complete-tasks'))
                        )

    @staticmethod
    def task_form_page(  # for creating or updating a task
        task_id = None,
        title='Task Form',
        action='',
        button_text='Submit',
        task_title='',
        description='',
        difficulty=1,
        deadline='',
        importance=1,
        dependencies = None,
        duration_hours=0,
        duration_minutes=0,
        category='Work',
        message=None,
        message_type=None
        ):
        return c.Titled(title,
            c.Div(
                c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
                    c.A('Back to Dashboard', href='/dashboard'),
                    c.Form(
                        c.Label('Title: ',
                        c.Input(type='text', name='title', value=task_title, required=True)
                ),
                  c.Br(),

                  c.Label('Description: ',
                  c.Textarea(description, name='description')
                ),

                c.Br(),

                c.Label('Difficulty: ',
                    c.Input(type='number', name='difficulty',
                            min=1, max=5, value=difficulty, required=True)
                ),

                c.Br(),

                c.Label('Deadline: ',
                    c.Input(type='datetime-local', name='deadline',
                            value=deadline, required=True)
                ),

                c.Br(),

                c.Label('Importance: ',
                    c.Input(type='number', name='importance',
                            min=1, max=5, value=importance, required=True)
                ),

                c.Br(),

                c.Label('Duration: ',
                    c.Input(type='number', name='duration_hours',
                            value=duration_hours, min=0),
                    c.Span(' hours '),
                    c.Input(type='number', name='duration_minutes',
                            value=duration_minutes, min=0, max=59),
                    c.Span(' minutes')
                ),

                c.Br(),

                c.Label('Category: ',
                    c.Input(type='radio', name='category',
                            value='Work',
                            checked=category=='Work',
                            required=True),
                    c.Span('Work'),

                    c.Input(type='radio', name='category',
                            value='Personal',
                            checked=category=='Personal'),
                    c.Span('Personal'),

                    c.Input(type='radio', name='category',
                            value='Business',
                            checked=category=='Business'),
                    c.Span('Business')
                ),

                c.Input(type='hidden',
                        name='dependencies',
                        id='dependencies',
                        value=",".join(dependencies) if dependencies else ""
                ),

                AutoSearch.render(
                    form_id='task-form',
                    hidden_input_id='dependencies',
                    entity='task',
                    search_id='dependencies',
                    mode='select'
                ),

                c.Button(button_text, type='submit', onclick="return confirm('Are you sure you want to save these changes?')" if task_id else None),

                method='POST',
                action=f'/update-task/{task_id}' if task_id else action,
                id='task-form'
            )
        )
    )

    @staticmethod
    def create_task_page(
         message=None,
         message_type=None,
         task_title='',
         description='',
         difficulty=1,
         deadline='',
         importance=1,
         duration_hours=0,
         duration_minutes=0,
         dependencies=None,
         category='Work'
         ):

     return Pages.task_form_page(
        title='Create Task',
        action='/create_task',
        button_text='Create Task',
        task_title=task_title,
        description=description,
        difficulty=difficulty,
        deadline=deadline,
        importance=importance,
        duration_hours=duration_hours,
        duration_minutes=duration_minutes,
        category=category,
        message=message,
        message_type=message_type,
        dependencies=dependencies 
    )

    @staticmethod
    def update_task_page(task, message=None, message_type=None):
        return Pages.task_form_page(
            task_id=task["_id"],
            title='Update Task',
            action='/update-task',
            button_text='Update Task',
            task_title=task["title"],
            description=task["description"],
            difficulty=task["difficulty"],
            deadline=task["deadline"].strftime("%Y-%m-%dT%H:%M"),
            importance=task["importance"],
            category=task["category"],
            dependencies=task.get("dependencies", []),
            duration_hours=task.get("duration", 0) // 60,
            duration_minutes=task.get("duration", 0) % 60,
            message=message,
            message_type=message_type,
            
    )

    @staticmethod 
    def task_action_page(  # for delete or complete tasks
         title='Task Action', 
         action='', 
         form_id='task-action-form', 
         hidden_input_id='selected_tasks', 
         button_text='Submit', 
         message=None, 
         message_type=None,
         onclick=None,
         mode = "select"
         ):
        return c.Titled(title,
        c.Div(
            c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
            c.A('Back to Dashboard', href='/dashboard'),

            c.Form(
                c.Input(
                    type='hidden',
                    name=hidden_input_id,
                    id=hidden_input_id
                ),

                AutoSearch.render(
                    form_id=form_id,
                    hidden_input_id=hidden_input_id,
                    mode=mode,
                    entity='task',
                    search_id= 'dependencies' 

                ),

                c.Button(button_text, type='submit', onclick=onclick if onclick else None),
                method='POST',
                action=action,
                id=form_id
                
            )
        )
    )

    @staticmethod
    def delete_tasks_page(message=None, message_type=None):
        return Pages.task_action_page(
            title='Delete Tasks',
            action='/delete-tasks',
            form_id='delete-task-form',
            hidden_input_id='selected_tasks',
            button_text='Delete Selected Tasks',
            message=message,
            message_type=message_type,
            onclick="return confirm('Are you sure you want to delete these tasks?')",
        )

    @staticmethod
    def complete_tasks_page(message=None, message_type=None):
        return Pages.task_action_page(
            title='Complete Tasks',
            action='/complete-tasks',
            form_id='complete-task-form',
            hidden_input_id='selected_tasks',
            button_text='Complete Selected Tasks',
            message=message,
            message_type=message_type
              )

    @staticmethod
    def search_update_tasks_page(message=None, message_type=None):
        return Pages.task_action_page(
            title='Search the tasks you want to update',
            form_id='search-update-task-form',
            hidden_input_id='selected_tasks',
            button_text='Select',
            message=message,
            message_type=message_type,
            mode="redirect"
        )



    @staticmethod
    def search_bar():
        return c.Div(c.Label('Dependencies: ', c.Input(type='search', id='search', placeholder='Search for the tasks')))

    @staticmethod
    def view_tasks_page(message=None, message_type=None, tasks=None):
        if tasks is None:
            tasks = []
        return c.Titled(
        'Task Schedule',
        c.A('Back to Dashboard', href='/dashboard'),
        c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),
            c.H2('Your Scheduled Tasks'),

            *[
                c.Form(
                    c.Button(
                        c.Div(
                            c.H3(task["title"]),
                            c.P(f'Deadline: {task["deadline"]}')
                        ),
                        type="submit"
                    ),
                    method="GET",
                    action=f"/task/{task['_id']}"
                )
                for task in tasks
            ]
        )
    )




                        