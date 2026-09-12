from services.query_service import QueryService
from typing import Optional
from core.app import rt
from utils.decorators_util import admin_required
from starlette.responses import JSONResponse



@admin_required   
@rt("/search-user", methods=["GET"])  
def search_user_by_email(query: Optional[str] = None):
    users = QueryService.search_user(query) if query else []
    print("FOUND:", users)
    return JSONResponse([
    {
        "id": user.user_id,
        "name": user.email
    }
    for user in users
])


@admin_required
@rt("/search-team", methods=["GET"])  
def search_team_by_name(query: Optional[str] = None):
    teams = QueryService.search_team(query) if query else []
    print("FOUND:", teams)
    return JSONResponse([
    {
        "id": team.team_id,
        "name": team.name
    }
    for team in teams
])


