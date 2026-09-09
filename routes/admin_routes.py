from services.user_service import UserService
from typing import Optional
from components.admin_components import Pages
from fasthtml import common as c
from core.app import rt


@rt('/create-company', methods=['GET'])
def get_create_company():
     return Pages.create_company_page()

@rt('/create-company', methods=['POST'])
def post_create_company():
    pass