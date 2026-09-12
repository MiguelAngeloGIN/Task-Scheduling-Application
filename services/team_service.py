from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.delete_crud import Delete_Sql
from crud.add_crud import Add_Sql
from database import models
from utils.query_util import query_handling
from library.validators import InputValidator
from utils.decorators_util import transaction



class TeamService:
    
    @staticmethod
    @transaction
    def create_team(team_name, company_id):
        InputValidator.validate_name(team_name)
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        return query_handling(Add_Sql.add_team, team_name, company_id,
                              error="Team with this name already exists."
                              )

    @staticmethod
    @transaction
    def delete_team(team_id):
        InputValidator.validate_id(team_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id
                                )
        if not team:
            raise ValueError("Team does not exist.")

        return query_handling(Delete_Sql.delete_sql, model=models.Team, team_id=team_id
                              )

    @staticmethod
    @transaction
    def add_user_to_team(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id
                               )
        if not user:
            raise ValueError("User does not exist.")

        user = user[0]

        team = Get_Sql.get_sql(models.Team, team_id=team_id)

        if not team:
            raise ValueError("Team does not exist.")

        if user.team_id == team_id:
            raise ValueError("User is already a member of this team.")

        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(Update_Sql.update_sql, model=models.User, 
                              user_id=user_id, team_id=team_id
                              )

    @staticmethod
    @transaction
    def remove_user_from_team(user_id):
        InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        return query_handling(Update_Sql.update_sql, model=models.User, 
                              user_id=user_id, team_id=None)


    @staticmethod
    @transaction
    def assign_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id
                               )

        if not user:
            raise ValueError("User does not exist.")
        user = user[0]

        team = Get_Sql.get_sql(models.Team, team_id=team_id
                               )

        if not team:
            raise ValueError("Team does not exist.")
        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id,
                              team_id=team_id, is_team_leader=True)

    @staticmethod
    @transaction
    def remove_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id)

        if not user:
            raise ValueError("User does not exist.")
        user = user[0]

        team = Get_Sql.get_sql(models.Team, team_id=team_id)

        if not team:
            raise ValueError("Team does not exist.")
        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError("User and team do not belong to the same company.")

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id, 
                              team_id=None, is_team_leader=False)
