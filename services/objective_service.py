
from crud.add_crud import Add_Sql
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from database import models
from library.validators import InputValidator
from utils.db_query_util import query_handling, transaction


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

        objective = Get_Sql.get_sql(models.Objective, objective_id=objective_id)
        if not objective:
            raise ValueError("Objective not found.")

        query_handling(Update_Sql.update_sql, model=models.Objective, objective_id=objective_id, archived=True, error="Failed to archive objective.")

        return True


    @staticmethod
    @transaction
    def calculate_objective_progress(objective_id):
        objective_id = InputValidator.validate_id(objective_id)

        objective = Get_Sql.get_sql(models.Objective, objective_id=objective_id)
        if not objective:
            raise ValueError("Objective not found.")
        
        tasks = Get_Sql.get_sql(models.Task, objective_id=objective_id)
        if not tasks:
            return 0

        completed_tasks = [task for task in tasks if task.status == "completed"]
        progress = (len(completed_tasks) / len(tasks)) * 100
        return round(progress)

  