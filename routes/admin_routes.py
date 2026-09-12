from services.company_service import CompanyService
from services.team_service import TeamService
from services.query_service import QueryService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.decorators_util import admin_required
from utils.json_util import parse_json_input

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


@rt('/create-company', methods=['GET'])
@admin_required
def get_create_company(request, message: Optional[str] = None, message_type: Optional[str] = None):
    try: 
         admin_payload = request.state.admin_payload
         user = QueryService.get_user(user_id=int(admin_payload['sub']))

         if user.company_id is not None:
              return c.RedirectResponse(
            '/admin-dashboard?message=You already belong to a company&message_type=error',
            status_code=302
        )
    except ValueError as e:
         return Pages.create_company_page(message, message_type)

    return Pages.create_company_page(message, message_type)

@rt('/create-company', methods=['POST'])
@admin_required
def post_create_company(request, name: str):
    try:
        admin_payload = request.state.admin_payload

        user = QueryService.get_user(user_id=int(admin_payload['sub']))

        if user.company_id is not None:
             return c.RedirectResponse(
            '/admin-dashboard?message=You already belong to a company&message_type=error',
            status_code=302
        )

    
        CompanyService.create_company(name=name,  user_id=int(admin_payload['sub']))
        return c.RedirectResponse(
            '/create-company?message=Company created successfully&message_type=success',
            status_code=302
        )
    except ValueError as e:
        return c.RedirectResponse(
            f'/create-company?message=Failed to create company: {str(e)}&message_type=error',
            status_code=302
        )


@rt('/invite-to-company', methods=['GET'])
@admin_required
def get_invite_user(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.invite_user_page(message=message, message_type=message_type)

@rt('/invite-to-company', methods=['POST'])
@admin_required
def post_invite_user(request, email: str):
        try:
             admin_payload = request.state.admin_payload
             admin_user = QueryService.get_user(user_id=int(admin_payload['sub']))

             company = QueryService.get_company(company_id=admin_user.company_id)
             company_id = company.company_id
        
             CompanyService.create_invitation(invited_by=int(admin_payload['sub']), company_id = company_id, invited_email=email)
             return c.RedirectResponse(f'/admin-dashboard?message=Invitation sent successfully&message_type=success', status_code=302)
        except ValueError as e:
            return Pages.invite_user_page(message=f'Failed to invite user: {str(e)}', message_type='error')


@rt('/accept-invitation', methods=['GET'])
def get_accept_invitation(request, token: str, message: Optional[str] = "", message_type: Optional[str] = ""):
      try:
        invitation = QueryService.get_invitation(token=token)
        invited_email = invitation.invited_email
        user = QueryService.get_user_by_email(email=invited_email)
        user_id = user.user_id
        company_id = invitation.company_id
        CompanyService.add_user_to_company( company_id=company_id, user_id=user_id, token=token)
        return c.RedirectResponse(f'/dashboard?message=Invitation accepted successfully&message_type=success', status_code=302)
      except ValueError as e:
        return Pages.accept_invite_page(message=f'{str(e)}', message_type='error')



@rt('/create-team', methods=['GET'])
@admin_required
def get_create_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.create_team_page(message=message, message_type=message_type)


@rt('/create-team', methods=['POST'])
@admin_required
def post_create_team(request, team_name: str):
        try:
            admin_payload = request.state.admin_payload
            company_id=QueryService.get_user(user_id=int(admin_payload['sub'])).company_id
            TeamService.create_team(team_name=team_name, company_id=company_id)
            return c.RedirectResponse(f'/admin-dashboard?message=Team created successfully&message_type=success', status_code=302)
        except ValueError as e:
            return Pages.create_team_page(message=f'Failed to create team: {str(e)}', message_type='error')



@rt('/deactivate-team', methods=['GET'])
@admin_required
def get_deactivate_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.deactivate_team_page(message=message, message_type=message_type)

@rt('/deactivate-team', methods=['POST'])
@admin_required
def post_deactivate_team(request, team_id: str):
        try:
            TeamService.deactivate_team(team_id=int(team_id))
            return c.RedirectResponse(f'/admin-dashboard?message=Team deactivated successfully&message_type=success', status_code=302)
        except ValueError as e:
            return Pages.deactivate_team_page(message=f'Failed to deactivate team: {str(e)}', message_type='error')


@rt('/add-to-team', methods=['GET'])
@admin_required
def get_add_to_team(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.user_team_page(message=message, message_type=message_type, 
                                    title='Add User to Team', action='/add-to-team'
                                    )

@rt('/add-to-team', methods=['POST'])
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
                                        title='Add User to Team', action='/add-to-team'
                                        )
        except ValueError as e:
            return Pages.user_team_page(message=f'Failed to add user to team: {str(e)}', message_type='error',
                                        title='Add User to Team', action='/add-to-team'
                                        )


@rt('/assign-team-leader', methods=['GET'])
@admin_required
def get_assign_team_leader(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.user_team_page(message=message, message_type=message_type, 
                                    warning = 'If the team already has a leader he will be replaced',
                                     title='Assign Team Leader', 
                                    action='/assign-team-leader', user_mode='select_one'
                                              )

@rt('/assign-team-leader', methods=['POST'])
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
                                        title='Assign Team Leader', action='/assign-team-leader', user_mode='select_one'
                                        )
        except ValueError as e:
            return Pages.user_team_page(message=f'Failed to assign team leader: {str(e)}', message_type='error',
                                        warning = 'If the team already has a leader he will be replaced',
                                        title='Assign Team Leader', action='/assign-team-leader', user_mode='select_one'
                                        )