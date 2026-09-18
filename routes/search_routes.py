from typing import Optional

from starlette.responses import JSONResponse

from core.app import rt
from permissions.decorators import (
    admin_required,
    auth_required,
    leader_required,
)
from services.query_service import QueryService


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


@rt("/search-all-users", methods=["GET"])
@admin_required
def search_all_users(request, query: Optional[str] = None):

    current_user_id = int(request.state.admin_payload["sub"]) if hasattr(request.state, "admin_payload") else None
    
    users = QueryService.search_all_users(query, exclude_user_id=current_user_id) if query else []
    

    return JSONResponse([
        {
            "id": user.user_id,
            "name": user.email
        }
        for user in users
    ])



@rt("/search-company-objectives", methods=["GET"])
@auth_required
def search_company_objectives(request, query: Optional[str] = None):

    payload =  request.state.user_payload
    user = QueryService.get_user(payload["sub"])
    company_id = user.company_id

    objectives = QueryService.get_objectives_by_company(company_id, query) if company_id else []
   
    return JSONResponse([
    {
        "id": objective.objective_id,
        "name": objective.name
    }
    for objective in objectives
])



@rt("/search-tasks-by-team-leader", methods=["GET"]) 
@leader_required
def search_tasks_by_team_leader(request, query: Optional[str] = None):

    user = request.state.user

    tasks = QueryService.get_tasks_by_team_leader(user.user_id, query) if user.user_id else []
   
    return JSONResponse([
    {
        "id": task.task_id,
        "name": task.name,
        "objective_id": task.objective_id,
        "objective": task.objective.name
    }
    for task in tasks
])

@rt("/search-tasks-for-dependency/{task_id}", methods=["GET"])
@leader_required
def search_tasks_for_dependency(request, task_id: int, query: Optional[str] = None):

    tasks = QueryService.get_tasks_for_dependency(
        task_id,
        query
    )

    return JSONResponse([
        {
            "id": task.task_id,
            "name": task.name,
            "objective": task.objective.name
        }
        for task in tasks
    ])


@rt("/search-tasks-by-user", methods=["GET"])
@auth_required
def search_tasks_by_user(request, query: Optional[str] = None):

    user_id = int(request.state.user_payload["sub"])

    tasks = QueryService.get_tasks_by_user(
        user_id,
        query
    )

    return JSONResponse([
        {
            "id": task.task_id,
            "name": task.name,
            "objective": task.objective.name
        }
        for task in tasks
    ])


@rt("/search-dependencies-by-task/{task_id}", methods=["GET"])
@leader_required
def search_dependencies_by_task(request, task_id: int, query: Optional[str] = None):

    dependencies = QueryService.get_dependencies_by_task(task_id, query)

    return JSONResponse([
        {
            "id": dependency.dependency_id,
            "name": dependency.dependency_task.name,
            "objective": dependency.dependency_task.objective.name
        }
        for dependency in dependencies
    ])


