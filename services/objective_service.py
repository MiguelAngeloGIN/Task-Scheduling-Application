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

    @staticmethod
    def create_objective(name, company_id, description):
        InputValidator.validate_name(name)
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)
        if not company:
            raise ValueError("Company is not registered.")
        company = company[0]

        objective = query_handling(Add_Sql.add_objective, name=name, company_id=company_id, description=description, error="Objective name already exists.")
        return objective
