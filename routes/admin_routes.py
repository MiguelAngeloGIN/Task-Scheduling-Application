from services.company_service import CompanyService
from services.team_service import TeamService
from services.query_service import QueryService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.decorators_util import admin_required


@rt('/create-company', methods=['GET'])
@admin_required
def get_create_company(request):
    admin_payload = request.state.admin_payload

    user = QueryService.get_user(user_id=int(admin_payload['sub']))

    if user.company_id is not None:
        return c.RedirectResponse(
            '/admin-dashboard?message=You already belong to a company&message_type=error',
            status_code=302
        )

    return Pages.create_company_page()


@rt('/create-company', methods=['POST'])
@admin_required
def post_create_company(request, name: str):
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


@rt('/admin-dashboard', methods=['GET'])
@admin_required
def get_admin_dashboard(request):
    return Pages.admin_dashboard_page(message=f'Welcome', 
                                      message_type='success')
   
    

@rt('/invite-to-company', methods=['GET'])
@admin_required
def get_invite_user(request):
        return Pages.invite_user_page()

@rt('/invite-to-company', methods=['POST'])
@admin_required
def post_invite_user(request, email: str):
        admin_payload = request.state.admin_payload
        admin_user = QueryService.get_user(user_id=int(admin_payload['sub']))

        company = QueryService.get_company(company_id=admin_user.company_id)
        company_id = company.company_id
        
        CompanyService.create_invitation(invited_by=int(admin_payload['sub']), company_id = company_id, invited_email=email)
        return c.RedirectResponse('/admin-dashboard?message=Invitation sent successfully&message_type=success', status_code=302)


@rt('/accept-invitation', methods=['GET'])
def get_accept_invitation(request, token: str):
      invitation = QueryService.get_invitation(token=token)
      invited_email = invitation.invited_email
      user = QueryService.get_user_by_email(email=invited_email)
      user_id = user.user_id
      company_id = invitation.company_id

      user = QueryService.get_user(user_id=user_id)
      CompanyService.add_user_to_company( company_id=company_id, user_id=user_id)
      return Pages.accept_invite_page()



@rt('/create-team', methods=['GET'])
@admin_required
def get_create_team(request):
        return Pages.create_team_page()


@rt('/create-team', methods=['POST'])
@admin_required
def post_create_team(request, team_name: str):
        admin_payload = request.state.admin_payload
        company_id=QueryService.get_user(user_id=int(admin_payload['sub'])).company_id
        TeamService.create_team(team_name=team_name, company_id=company_id)
        return c.RedirectResponse('/admin-dashboard?message=Team created successfully&message_type=success', status_code=302)



@rt('/delete-team', methods=['GET'])
@admin_required
def get_delete_team(request):
        return Pages.delete_team_page()

@rt('/delete-team', methods=['POST'])
@admin_required
def post_delete_team(request, team_id: str):
        TeamService.delete_team(team_id=int(team_id))
        return c.RedirectResponse('/admin-dashboard?message=Team deleted successfully&message_type=success', status_code=302)
