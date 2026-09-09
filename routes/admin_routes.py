from services.admin_service import AdminService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt


@rt('/create-company', methods=['GET'])
def get_create_company():
     return Pages.create_company_page()

@rt('/create-company', methods=['POST'])
def post_create_company(name: str):
    try:
        AdminService.create_company(name=name)

        return c.RedirectResponse('/create-company?message=Company created successfully&message_type=success', status_code=302)
    except ValueError as e:
        return Pages.create_company_page(
            message=str(e),
            message_type="error",
            name=name
        )

