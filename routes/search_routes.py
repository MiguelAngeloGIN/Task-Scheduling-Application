from services.query_service import QueryService
from typing import Optional
from core.app import rt
from utils.decorators_util import admin_required
from starlette.responses import JSONResponse


 
@rt("/search-user", methods=["GET"])  
@admin_required
def search_user_by_email(request, query: Optional[str] = None):

    admin_payload = request.state.admin_payload
    admin = QueryService.get_user(int(admin_payload["sub"]))
    company_id = admin.company_id

    users = QueryService.search_user(query, company_id) if query else []
    print("FOUND:", users)
    return JSONResponse([
    {
        "id": user.user_id,
        "name": user.email
    }
    for user in users
])


@rt("/search-team", methods=["GET"]) 
@admin_required
def search_team_by_name(request, query: Optional[str] = None):

    admin_payload = request.state.admin_payload
    admin = QueryService.get_user(int(admin_payload["sub"]))
    company_id = admin.company_id

    teams = QueryService.search_team(query, company_id) if query else []
    print("FOUND:", teams)
    return JSONResponse([
    {
        "id": team.team_id,
        "name": team.name
    }
    for team in teams
])


