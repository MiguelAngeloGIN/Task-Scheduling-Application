from services.objective_service import ObjectiveService 
from typing import Optional
from components.company_team_objective_components import Pages
from fasthtml import common as c
from core.app import rt
from services.query_service import QueryService
from permissions.decorators import admin_required






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


@rt('/admin/objective/manage', methods= ['GET'])
@admin_required
def get_manage_objectives(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.manage_objectives_page(message=message, message_type=message_type)

