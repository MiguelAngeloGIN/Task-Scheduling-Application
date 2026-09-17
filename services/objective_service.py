from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.add_crud import Add_Sql
from database import models
from utils.db_query_util import query_handling
import secrets
from library.validators import InputValidator
from datetime import datetime, timedelta, timezone
from services.email_service import EmailService
from utils.db_query_util import transaction


class ObjectiveService:

    @staticmethod
    @transaction
    def create_objective(name, company_id, description):
        InputValidator.validate_name(name)
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)
        if not company:
            raise ValueError("Company is not registered.")
        company = company[0]

        objective = query_handling(Add_Sql.add_objective, name=name, company_id=company_id, description=description, error="Objective name already exists.")
        return objective

    @staticmethod
    @transaction
    def archive_objective(objective_id):
        objective_id = InputValidator.validate_id(objective_id)

        old_objective = Get_Sql.get_sql(models.Objective, objective_id=objective_id)
        if not old_objective:
            raise ValueError("Objective not found.")
        old_objective = old_objective[0]

        Update_Sql.update_sql(models.Objective, objective_id=objective_id, archived=True)

        return True

  