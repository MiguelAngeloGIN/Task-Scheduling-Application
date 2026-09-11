from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.add_crud import Add_Sql
from database import models
from utils.query_util import query_handling
import secrets
from library.validators import InputValidator
from datetime import datetime, timedelta, timezone
from services.email_service import EmailService


class ObjectiveService:

    def create_objective(title: str, description: str, company_id: int):