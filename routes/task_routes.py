from typing import Optional

from fasthtml import common as c

from components.task_components import Pages
from core.app import rt
from permissions.decorators import auth_required, leader_required
from services.query_service import QueryService
from services.task_service import TaskService
from utils.json_util import parse_json_input


@rt('/task/create', methods=['GET'])
@leader_required
def get_create_task(request, message: Optional[str] = None, message_type: Optional[str] = None):

    return Pages.create_task_page(
        message=message,
        message_type=message_type
    )


@rt('/task/create', methods=['POST'])
@leader_required
def post_create_task(request, name: str, description: str, deadline: str, importance: int, objective_id: int):

    try:
          user_id = int(request.state.user_payload['sub'])
        
          team = QueryService.get_team_by_leader(user_id)


          TaskService.create_task(name=name, description=description, deadline=deadline, importance=importance, 
                            author_id=user_id, team_id=team.team_id, objective_id=objective_id)
          

          return c.RedirectResponse('/leader-dashboard?&message=Task created successfully&message_type=success', status_code = 302)
    
    except Exception as e:
         return Pages.create_task_page(message=str(e),message_type="error", task_name=name, description=description,
                                        deadline=deadline, importance=importance)



@rt('/tasks/manage', methods=['GET'])
@leader_required
def get_manage_tasks(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.manage_tasks_page(message=message, message_type=message_type)


@rt("/task/manage/action/{task_id}")
@leader_required
def task_action_page(request, task_id: int, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.manage_tasks_action_page(task_id=task_id, message=message, message_type=message_type)



@rt('/task/update/{task_id}', methods=['GET'])
@leader_required
def get_update_task(request, task_id: int, message: Optional[str] = None, message_type: Optional[str] = None):
    try:
        task = QueryService.get_task(task_id)
    except Exception as e:
        return c.RedirectResponse(f"/tasks/manage?message={str(e)}&message_type=error",
                                  status_code=302)

    return Pages.update_task_page(task=task, message=message, message_type=message_type)


@rt('/task/update/{task_id}', methods=['POST'])
@leader_required
def post_update_task(request, task_id: int, name: str, description: str, deadline: str,
                      importance: int, message_type: Optional[str] = None, message: Optional[str] = None,
                      ):
    try:
        TaskService.update_task(task_id, name=name, description=description, deadline=deadline, importance=importance)
        return c.RedirectResponse('/leader-dashboard?&message=Task updated successfully&message_type=success', status_code = 302)
    except Exception as e:
        task = QueryService.get_task(task_id)
        return Pages.update_task_page(task=task, message=str(e), message_type="error")


@rt('/task/dependencies/add/{task_id}', methods=['GET'])
@leader_required
def get_add_dependency(request, task_id: int, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.add_dependency_page(task_id=task_id, message=message, message_type=message_type)
    

@rt('/task/dependencies/add/{task_id}', methods=['POST'])
@leader_required
def post_add_dependencies(request, task_id: int, dependency_id: str):
    try:
        
        dependency_ids = parse_json_input(dependency_id)

        TaskService.add_dependencies(dependant_id=task_id, dependency_ids=dependency_ids)

        return c.RedirectResponse('/leader-dashboard?&message=Dependencies added successfully&message_type=success', status_code = 302)
    except Exception as e:
        return c.RedirectResponse(f'/leader-dashboard?&message={str(e)}&message_type=error', status_code = 302)



@rt('/task/dependencies/remove/{task_id}', methods=['GET'])
@leader_required
def get_remove_dependency(request, task_id: int, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.remove_dependencies_page(task_id=task_id, message=message, message_type=message_type)


@rt('/task/dependencies/remove/{task_id}', methods=['POST'])
@leader_required
def post_remove_dependencies(request, task_id: int, dependency_ids: str):
    try:
        dependency_ids_list = parse_json_input(dependency_ids)
        TaskService.remove_dependencies(task_id=task_id, dependency_ids_pk=dependency_ids_list)
        return c.RedirectResponse('/leader-dashboard?&message=Dependencies removed successfully&message_type=success', status_code = 302)
    except Exception as e:
        return c.RedirectResponse(f'/leader-dashboard?&message={str(e)}&message_type=error', status_code = 302)



@rt('/task/complete', methods=['GET'])
@auth_required
def get_complete_task(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.complete_task_page(message=message, message_type=message_type)

@rt('/task/complete', methods=['POST'])
@auth_required
def post_complete_task(request, task_id: int):
    try:
        author_id = int(request.state.user_payload["sub"])

        TaskService.complete_task(task_id=task_id,
                                  author_id=author_id)

        user = QueryService.get_user(user_id=author_id)

        if user.led_team_id:
            redirect = "/leader-dashboard"
        else:
            redirect = "/dashboard"

        return c.RedirectResponse(f'{redirect}?message=Task completed successfully&message_type=success',
                                  status_code=302)

    except Exception as e:
        return Pages.complete_task_page(message=str(e), message_type="error")


@rt('/task/remove/{task_id}', methods=['POST'])
@leader_required
def post_remove_task(request, task_id: int):
    try:
        author = request.state.user
        author_id = author.user_id
        
        TaskService.delete_task(task_id=task_id, author_id=author_id)
        return c.RedirectResponse('/leader-dashboard?&message=Task removed successfully&message_type=success', status_code = 302)
    except Exception as e:
        return c.RedirectResponse(f'/leader-dashboard?&message={str(e)}&message_type=error', status_code = 302)





