from services.company_service import CompanyService
from services.team_service import TeamService
from services.query_service import QueryService
from typing import Optional
from components.company_team_objective_components import Pages
from fasthtml import common as c
from core.app import rt
from permissions.decorators import admin_required
from utils.json_util import parse_json_input


@rt('/admin/company/create', methods=['GET'])
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

@rt('/admin/company/create', methods=['POST'])
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
            '/admin-dashboard?message=Company created successfully&message_type=success',
            status_code=302
        )
    except ValueError as e:
        return c.RedirectResponse(
            f'/admin-dashboard?message=Failed to create company: {str(e)}&message_type=error',
            status_code=302
        )

@rt('/admin/company/invite', methods=['GET'])
@admin_required
def get_invite_user(request, message: Optional[str] = None, message_type: Optional[str] = None):
        return Pages.invite_user_page(message=message, message_type=message_type)

@rt('/admin/company/invite', methods=['POST'])
@admin_required
def post_invite_user(request, user_id: str):
    try:
        admin_payload = request.state.admin_payload
        admin_id = int(admin_payload['sub'])

        admin_user = QueryService.get_user(user_id=admin_id)

        company = QueryService.get_company(company_id=admin_user.company_id)
        company_id = company.company_id

        user = QueryService.get_user(user_id=int(user_id))

        CompanyService.create_invitation(invited_by=admin_id, company_id=company_id,
                                         invited_email=user.email
        )

        return c.RedirectResponse(
            '/admin-dashboard?message=Invitation sent successfully&message_type=success',
            status_code=302
        )

    except ValueError as e:
        return Pages.invite_user_page(message=f'Failed to invite user: {str(e)}',
                                      message_type='error'
        )


@rt('/accept-invitation', methods=['GET'])
def get_accept_invitation(request, token: str, message: Optional[str] = "", message_type: Optional[str] = ""):
      try:
        invitation = QueryService.get_invitation(token=token)
        invited_email = invitation.invited_email
        user = QueryService.get_user_by_email(email=invited_email)
        user_id = user.user_id
        company_id = invitation.company_id
        CompanyService.accept_invitation( company_id=company_id, user_id=user_id, token=token)
        return c.RedirectResponse(f'/dashboard?message=Invitation accepted successfully&message_type=success', status_code=302)
      except ValueError as e:
        return Pages.accept_invite_page(message=f'{str(e)}', message_type='error')








