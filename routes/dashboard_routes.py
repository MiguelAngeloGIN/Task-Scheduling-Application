
from typing import Optional

from fasthtml import common as c

from components.company_team_objective_components import Pages
from components.task_components import Pages as TaskPages
from core.app import rt
from permissions.decorators import admin_required, auth_required, leader_required
from services.query_service import QueryService


@rt('/admin-dashboard', methods=['GET'])
@admin_required
def get_admin_dashboard(request, message: Optional[str] = None, message_type: Optional[str] = None):
    try:
        admin_payload = request.state.admin_payload
        user = QueryService.get_user(user_id=int(admin_payload['sub']))

        if user.company_id is None:
            return c.RedirectResponse(
                '/login?message=You do not belong to any company&message_type=error',
                status_code=302
            )
        
    except ValueError as e:
        return c.RedirectResponse(
            f'/login?message=Failed to load admin dashboard: {str(e)}&message_type=error',
            status_code=302
        )

    return Pages.admin_dashboard_page(message=message, 
                                      message_type=message_type)

@rt('/objective-dashboard', methods=['GET'])
@admin_required
def get_objective_dashboard(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.objective_dashboard_page(message=message, message_type=message_type)



@rt('/dashboard')
@auth_required
def get_dashboard(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return TaskPages.dashboard_page(message=message, message_type=message_type)

@rt('/leader-dashboard', methods=['GET'])
@leader_required
def get_leader_dashboard(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return TaskPages.leader_dashboard_page(message=message, message_type=message_type)





