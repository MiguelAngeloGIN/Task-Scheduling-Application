from services.task_service import TaskService
from datetime import timezone, datetime
from typing import Optional
from components.task_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.jwt_util import JWTUtils
from starlette.responses import JSONResponse
from utils.json_util import parse_json_input



@rt('/dashboard')
def get_dashboard(message: Optional[str] = None, message_type: Optional[str] = None):
    return Pages.dashboard_page(message=message, message_type=message_type)
