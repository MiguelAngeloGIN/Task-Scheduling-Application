from fasthtml import common as c
from components.search_component import AutoSearch

class Pages:
    @staticmethod
    def dashboard_page(message=None, message_type=None):
        return c.Titled('Dashboard',
                     c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P()),
                        c.P('Welcome to your dashboard!'),
                        c.Div(c.Form(c.Button('Logout', type='submit'), method='POST', action='auth/logout')),
                        c.Div(c.Form(c.Button('VIEW TASKS', type = "submit"), method='GET', action='/view_tasks')),
                        c.Div(c.Form(c.Button('COMPLETE TASKS', type = "submit"), method='GET', action='/complete-tasks'))
                        )

    @staticmethod
    def leader_dashboard_page(message=None, message_type=None):
        return c.Titled('Dashboard',
                     c.Div(c.P(f'{message}', cls=f"message {message_type}") if message else c.P()),
                        c.P('Welcome to your dashboard!'),
                        c.Div(c.Form(c.Button('Logout', type='submit'), method='POST', action='auth/logout')),
                        c.Div(c.Form(c.Button('CREATE TASK', type = "submit"), method='GET', action='/task/create')),
                        c.Div(c.Form(c.Button('MANAGE TASKS', type="submit"), method='GET', action='/tasks/manage')),
                        c.Div(c.Form(c.Button('COMPLETE TASK', type = "submit"),method='GET', action=f'/task/complete')),
                        c.Div(c.Form(c.Button('VIEW OBJECTIVES SCHEDULE', type = "submit"), method='GET', action='/admin/objective/view'))
                        )





    @staticmethod
    def task_form_page(  # for creating or updating a task
        task_id = None,
        title='Task Form',
        action='',
        button_text='Submit',
        task_name='',
        description='',
        deadline='',
        importance=1,
        select_objective = True,
        message=None,
        message_type=None
        ):

        objective_field = (AutoSearch.render(
                            form_id="task-form",
                            hidden_input_id="objective_id",
                            entity="company-objectives",
                            search_id="objective-search",
                            label="Objective:",
                            mode="select_one"
                        )
                        if select_objective else "")

        
        return c.Titled(title,
            c.Div(
                c.P(f'{message}', cls=f"message {message_type}") if message else "",
                    c.A('Back to Dashboard', href='/leader-dashboard'),
                    c.Form(
                        c.Label('Name: ',
                        c.Input(type='text', name='name', value=task_name, required=True)
                ),
                  c.Br(),

                  c.Label('Description: ',
                  c.Textarea(description, name='description')
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

                objective_field,
              
                c.Button(button_text, type='submit', onclick="return confirm('Are you sure you want to save these changes?')" if task_id else None),

                method='POST',
                action=f'/task/update/{task_id}' if task_id else action,
                id='task-form'
            )
        )
    )

    @staticmethod
    def create_task_page(
         message=None,
         message_type=None,
         task_name='',
         description='',
         deadline='',
         importance=1
         ):

     return Pages.task_form_page(
        title='Create Task',
        action='/task/create',
        button_text='Create Task',
        task_name=task_name,
        description=description,
        deadline=deadline,
        importance=importance,
        message=message,
        message_type=message_type
    )

    @staticmethod
    def manage_tasks_page(message=None, message_type=None):
        return c.Titled(
        "Manage Tasks",

        c.Div(
            c.P(f"{message}", cls=f"message {message_type}") if message else "",

            c.Form(
                AutoSearch.render(
                    form_id="manage-tasks-form",
                    hidden_input_id="task_id",
                    entity="tasks-by-team-leader",
                    search_id="task-search",
                    label="Task:",
                    mode="redirect",
                    redirect_url=f"/task/manage/action"
                )
            ),

            c.A("Dashboard", href="/leader-dashboard")
        )
    )


    @staticmethod
    def manage_tasks_action_page(task_id, message=None, message_type=None):
        return c.Div(c.Titled('Select Task Action',
            c.Div(c.Form(c.Button('UPDATE TASK', type = "submit"), method='GET', action=f'/task/update/{task_id}')),
            c.Div(c.Form(c.Button('ADD DEPENDENCIES', type = "submit"), method='GET', action=f'/task/dependencies/add/{task_id}')),
            c.Div(c.Form(c.Button('REMOVE DEPENDENCIES', type = "submit"), method='GET', action=f'/task/dependencies/remove/{task_id}')),
            c.Div(c.Form(c.Button('DELETE TASK', type = "submit", onclick = "return confirm('Are you sure you want to delete this task?')"),
                                    method='POST', action=f'/task/delete/{task_id}')),
            c.Div(c.A('Back to Dashboard', href='/leader-dashboard'))
        ))



    @staticmethod
    def update_task_page(task, message=None, message_type=None):
        return Pages.task_form_page(
            task_id=task.task_id,
            title='Update Task',
            action=f'/task/update/{task.task_id}',
            button_text='Update Task',
            task_name=task.name,
            description=task.description,
            deadline=task.deadline.strftime("%Y-%m-%dT%H:%M"),
            importance=task.importance,
            select_objective= False,
            message=message,
            message_type=message_type
            )

    @staticmethod
    def add_dependency_page(task_id: int, message=None, message_type=None):

        return c.Titled("Add Dependency",

        c.Form(
            AutoSearch.render(
                form_id="dependency-form",
                hidden_input_id="dependency_id",
                entity=f"tasks-for-dependency/{task_id}",
                search_id="dependency-search",
                label="Dependency Task:",
                mode="select"
            ),

            c.Button("Add Dependency", type="submit"),

            method="POST",
            action=f"/task/dependencies/add/{task_id}",
            id="dependency-form"
        )
    )

    @staticmethod
    def complete_task_page(message=None, message_type=None):  

        return c.Titled("Complete Task",

        c.Form(
            AutoSearch.render(
                form_id="complete-task-form",
                hidden_input_id="task_id",
                entity="tasks-by-user",
                search_id="task-search",
                label="Task:",
                mode="select_one"
            ),

            c.Button("Complete Task", type="submit"),

            method="POST",
            action="/task/complete",
            id="complete-task-form"
        )
    )


    @staticmethod
    def remove_dependencies_page(task_id: int, message=None, message_type=None):  
    
            return c.Titled("Remove Dependencies Task",
    
            c.Form(
                AutoSearch.render(
                    form_id="remove-dependency-task-form",
                    hidden_input_id="dependency_ids",
                    entity=f"dependencies-by-task/{task_id}",
                    search_id="task-search",
                    label="Task:",
                    mode="select"
                ),
    
                c.Button("Remove Dependencies", type="submit", onclick=f"return confirm('Are you sure you want to remove this dependency?');"),
    
                method="POST",
                action=f"/task/dependencies/remove/{task_id}",
                id="remove-dependency-task-form"
            )
        )







    @staticmethod
    def view_tasks_schedule_page(message=None, message_type=None, tasks=None, dashboard_link='/dashboard'):
        if tasks is None:
            tasks = []

        return c.Titled('Task Schedule',
                        c.A('Back to Dashboard',href=dashboard_link
                            ),

                         c.Div(
                             c.P(f'{message}', cls=f"message {message_type}") if message else c.P(),

                         c.H2('Your Scheduled Tasks'),

            *[
                c.Div(
                    c.H3(f"{task.objective.name}: {task.name}"),

                    c.P(
                        f"Deadline: {task.deadline}"
                    ),
                    cls="task-card"
                )
                for task in tasks
            ]
        )
    )

    

    
    

    



