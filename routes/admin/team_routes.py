from services.company_service import CompanyService
from services.team_service import TeamService
from services.query_service import QueryService
from typing import Optional
from components.company_team_objective_components import Pages
from fasthtml import common as c
from core.app import rt
from permissions.decorators import admin_required
from utils.json_util import parse_json_input


@rt('/admin/team/create', methods=['GET'])
@admin_required
def get_create_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.create_team_page(message=message, message_type=message_type)

@rt('/admin/team/create', methods=['POST'])
@admin_required
def post_create_team(request, team_name: str):
        try:
            admin_payload = request.state.admin_payload
            company_id=QueryService.get_user(user_id=int(admin_payload['sub'])).company_id
            TeamService.create_team(team_name=team_name, company_id=company_id)
            return c.RedirectResponse(f'/admin-dashboard?message=Team created successfully&message_type=success', status_code=302)
        except ValueError as e:
            return Pages.create_team_page(message=f'Failed to create team: {str(e)}', message_type='error')



@rt('/admin/team/deactivate', methods=['GET'])
@admin_required
def get_deactivate_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.deactivate_team_page(message=message, message_type=message_type)

@rt('/admin/team/deactivate', methods=['POST'])
@admin_required
def post_deactivate_team(request, team_id: str):
        try:
            TeamService.deactivate_team(team_id=int(team_id))
            return c.RedirectResponse(f'/admin-dashboard?message=Team deactivated successfully&message_type=success', status_code=302)
        except ValueError as e:
            return Pages.deactivate_team_page(message=f'Failed to deactivate team: {str(e)}', message_type='error')


@rt('/admin/team/add', methods=['GET'])
@admin_required
def get_add_to_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.user_team_page(message=message, message_type=message_type, 
                                    title='Add User to Team', action='/admin/team/add'
                                    )

@rt('/admin/team/add', methods=['POST'])
@admin_required
def post_add_to_team(request, user_id: str, team_id: str):
        try:
            admin_payload = request.state.admin_payload
            company_id=QueryService.get_user(user_id=int(admin_payload['sub'])).company_id
            user_ids = parse_json_input(user_id)

            if not user_ids:
                raise ValueError("Please select at least one user email from the dropdown")

            if not team_id:
                raise ValueError("Please select a team from the dropdown")
           

            team = QueryService.get_company_team(team_id=int(team_id), company_id=company_id)

            for selected_user_id in user_ids:

                 if not selected_user_id:
                     raise ValueError("Please select at least one user email from the dropdown")
                 
                 user = QueryService.get_company_user(user_id=int(selected_user_id), company_id=company_id)
           
                 TeamService.add_user_to_team(team_id=int(team.team_id), user_id=int(user.user_id))

        
            return Pages.user_team_page(message=f'Users added to team successfully', message_type='success', 
                                        title='Add User to Team', action='/admin/team/add'
                                        )
        except ValueError as e:
            return Pages.user_team_page(message=f'Failed to add user to team: {str(e)}', message_type='error',
                                        title='Add User to Team', action='/admin/team/add'
                                        )


@rt('/admin/team/remove', methods=['GET'])
@admin_required
def get_remove_from_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.user_team_page(message=message, message_type=message_type, 
                                    warning = 'If the team leader is removed, the team will be without a leader',
                                     title='Remove User from Team', action='/admin/team/remove', user_mode='select_one'
                                              )

@rt('/admin/team/remove', methods=['POST'])
@admin_required
def post_remove_from_team(request, user_id: str, team_id: str):
        try:
            admin_payload = request.state.admin_payload
            admin = QueryService.get_user(int(admin_payload['sub']))
            company_id = admin.company_id

            if not user_id:
                raise ValueError("Please select one user email from the dropdown")

            if not team_id:
                raise ValueError("Please select a team from the dropdown")

            QueryService.get_company_team(team_id=team_id, company_id=company_id)
            QueryService.get_company_user(user_id=user_id, company_id=company_id)

            TeamService.remove_user_from_team(team_id=team_id, user_id=user_id)

            return Pages.user_team_page(message=f'User removed from team successfully', message_type='success', 
                                        warning = 'Removing a user from the team will leave the team without that member',
                                        title='Remove User from Team', action='/admin/team/remove', user_mode='select_one'
                                        )
        except ValueError as e:
            return Pages.user_team_page(message=f'Failed to remove user from team: {str(e)}', message_type='error',
                                        warning = 'Removing a user from the team will leave the team without that member',
                                        title='Remove User from Team', action='/admin/team/remove', user_mode='select_one'
                                        )




@rt('/admin/team/assign-leader', methods=['GET'])
@admin_required
def get_assign_team_leader(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.user_team_page(message=message, message_type=message_type, 
                                    warning = 'If the team already has a leader he will be replaced',
                                     title='Assign Team Leader', 
                                    action='/admin/team/assign-leader', user_mode='select_one'
                                              )

@rt('/admin/team/assign-leader', methods=['POST'])
@admin_required
def post_assign_team_leader(request, user_id: str, team_id: str):
        
        try:
            admin_payload = request.state.admin_payload
            admin = QueryService.get_user(int(admin_payload['sub']))
            company_id = admin.company_id

            if not user_id:
                raise ValueError("Please select one user email from the dropdown")

            if not team_id:
                raise ValueError("Please select a team from the dropdown")

            team_id_int = int(team_id)

            user_id_int = int(user_id)

            QueryService.get_company_team(team_id=team_id_int, company_id=company_id)

            QueryService.get_company_user(user_id=user_id_int, company_id=company_id)

            TeamService.assign_team_leader(team_id=team_id_int, user_id=user_id_int)

        
            return Pages.user_team_page(message=f'User assigned as team leader successfully', message_type='success', 
                                        warning = 'If the team already has a leader he will be replaced',
                                        title='Assign Team Leader', action='/admin/team/assign-leader', user_mode='select_one'
                                        )
        except ValueError as e:
            return Pages.user_team_page(message=f'Failed to assign team leader: {str(e)}', message_type='error',
                                        warning = 'If the team already has a leader he will be replaced',
                                        title='Assign Team Leader', action='/admin/team/assign-leader', user_mode='select_one'
                                        )


@rt('/admin/team/remove-leader', methods=['GET'])
@admin_required
def get_remove_team_leader(request, message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.user_team_page(message=message, message_type=message_type, 
                                warning = 'After removing the team leader you will be required to assign a new leader',
                                title='Remove Team Leader', action='/admin/team/remove-leader', user_mode='select_one'
                                )

@rt('/admin/team/remove-leader', methods=['POST'])
@admin_required
def post_remove_team_leader(request, user_id: str, team_id: str):
    try:
        admin_payload = request.state.admin_payload
        admin = QueryService.get_user(int(admin_payload['sub']))
        company_id = admin.company_id

        if not user_id:
            raise ValueError("Please select one user email from the dropdown")

        if not team_id:
            raise ValueError("Please select a team from the dropdown")

        team_id_int = int(team_id)
        user_id_int = int(user_id)

        QueryService.get_company_team(team_id=team_id_int, company_id=company_id)
        QueryService.get_company_user(user_id=user_id_int, company_id=company_id)


        TeamService.remove_team_leader(team_id=team_id_int, user_id=user_id_int)

        return Pages.user_team_page(message=f'Team leader removed successfully', message_type='success', 
                                    warning = 'After removing the team leader you will be required to assign a new leader',
                                    title='Remove Team Leader', action='/admin/team/remove-leader', user_mode='select_one'
                                    )
    except ValueError as e:
        return Pages.user_team_page(message=f'Failed to remove team leader: {str(e)}', message_type='error',
                                    warning = 'After removing the team leader you will be required to assign a new leader',
                                    title='Remove Team Leader', action='/admin/team/remove-leader', user_mode='select_one'
                                    )




@rt("/admin/team/view", methods=["GET"])
@admin_required
def view_teams(request):
    try:
        admin_payload = request.state.admin_payload
        admin_id = int(admin_payload["sub"])

        teams = QueryService.get_company_teams(admin_id)

        return Pages.view_teams_page(teams)

    except ValueError as e:
        return Pages.admin_dashboard_page(
            message=str(e),
            message_type="error"
        )

