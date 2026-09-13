from services.company_service import CompanyService
from services.team_service import TeamService
from services.query_service import QueryService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.decorators_util import admin_required


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


