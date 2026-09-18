from services.objective_service import ObjectiveService 
from services.task_service import TaskService
from typing import Optional
from components.company_team_objective_components import Pages
from components.task_components import Pages as TaskPages
from fasthtml import common as c
from core.app import rt
from services.query_service import QueryService
from permissions.decorators import admin_required, auth_required






@rt('/admin/objective/create', methods= ['GET'])
@admin_required
def get_create_objective(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.create_objective_page(message=message, message_type=message_type)

@rt('/admin/objective/create', methods= ['POST'])
@admin_required
def post_create_objective(request, objective_name: str, description: Optional[str] = None):
    try:
        admin_payload = request.state.admin_payload
        user = QueryService.get_user(user_id=int(admin_payload['sub']))
        company_id = user.company_id
        ObjectiveService.create_objective(name=objective_name, description=description, company_id=company_id)
        return c.RedirectResponse(
            '/objective-dashboard?message=Objective created successfully&message_type=success',
            status_code=302
        )
    except ValueError as e:
        return Pages.create_objective_page(message=f'Failed to create objective: {str(e)}', message_type='error')


@rt('/admin/objective/archive', methods= ['GET'])
@admin_required
def get_archive_objective(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.archive_objective_page(message=message, message_type=message_type)

@rt('/admin/objective/archive', methods= ['POST'])
@admin_required
def post_archive_objective(request, name: str, objective_id: int):
    try:
        admin_payload = request.state.admin_payload
        user = QueryService.get_user(user_id=int(admin_payload['sub']))
        company_id = user.company_id
        ObjectiveService.archive_objective(objective_id=objective_id)
        return c.RedirectResponse(
            '/objective-dashboard?message=Objective archived successfully&message_type=success',
            status_code=302
        )
    except ValueError as e:
        return Pages.archive_objective_page(message=f'Failed to archive objective: {str(e)}', message_type='error')


@rt('/admin/objective/view', methods=['GET'])
@auth_required
def view_objectives(
    request,
    message: Optional[str] = None,
    message_type: Optional[str] = None
):
    try:
        payload = request.state.user_payload
        user_id = int(payload["sub"])

        user = QueryService.get_user(user_id=user_id)
        company_id = user.company_id

        objectives = QueryService.get_objectives_by_company(company_id=company_id)

        progress = {
            objective.objective_id:
                ObjectiveService.calculate_objective_progress(
                    objective.objective_id
                )
            for objective in objectives
        }

        return Pages.view_objectives_page(
            objectives=objectives,
            progress=progress,
            message=message,
            message_type=message_type
        )

    except ValueError as e:
        return Pages.view_objectives_page(
            objectives=[],
            progress={},
            message=str(e),
            message_type="error"
        )

@rt('/task/view-schedule/{objective_id}', methods=['GET'])
@auth_required
def get_view_schedule(request, objective_id: int, message: Optional[str] = None, message_type: Optional[str] = None):

    payload = request.state.user_payload
    user_id = int(payload["sub"])

    team_leader = QueryService.is_team_leader(user_id=user_id)

    if team_leader:
        dashboard_link = '/leader-dashboard'
    else:
        dashboard_link = '/dashboard'

    tasks = TaskService.get_sorted_tasks_by_objective(objective_id)

    return TaskPages.view_tasks_schedule_page(message=message, message_type=message_type, tasks=tasks, 
                                          dashboard_link=dashboard_link)