from services.admin_service import AdminService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.jwt_util import JWTUtils


@rt('/create-company', methods=['GET'])
def get_create_company(request):
     try:
         JWTUtils.verify_admin(request)
         return Pages.create_company_page()
     except ValueError as e:
         return c.RedirectResponse(f'/login?message={str(e)}&message_type=error', status_code=302)


@rt('/create-company', methods=['POST'])
def post_create_company(request, name: str):
    try:
        payload = JWTUtils.verify_admin(request)
        AdminService.create_company(name=name, user_id=int(payload['sub']))

        return c.RedirectResponse('/create-company?message=Company created successfully&message_type=success', status_code=302)
        
    except ValueError as e:
        return Pages.create_company_page(
            message=str(e),
            message_type="error",
            name=name
        )

