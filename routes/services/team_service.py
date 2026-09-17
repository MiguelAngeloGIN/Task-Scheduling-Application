from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.delete_crud import Delete_Sql
from crud.add_crud import Add_Sql
from services.query_service import QueryService
from database import models
from utils.db_query_util import query_handling
from library.validators import InputValidator
from utils.db_query_util import transaction




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
    def deactivate_team(team_id):
        InputValidator.validate_id(team_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id
                                )
        if not team:
            raise ValueError("Team does not exist.")

        return query_handling(Update_Sql.update_sql, model=models.Team, team_id=team_id, is_active=False
                              )

    @staticmethod
    @transaction
    def add_user_to_team(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        users = Get_Sql.get_sql(models.User, user_id=user_id
                               )
        if not users:
            raise ValueError("User does not exist.")

        user = users[0]

        if user.is_admin:
            raise ValueError("Admin users cannot be added to a team.")

        team = Get_Sql.get_sql(models.Team, team_id=team_id)

        if not team:
            raise ValueError("Team does not exist.")
        
        membership = Get_Sql.get_sql(models.TeamMember, user_id=user_id, team_id=team_id)

        if  membership:
           raise ValueError("User is already a member of this team.")

        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(Add_Sql.add_team_member, team_id, user_id
                              )

    @staticmethod
    @transaction
    def remove_user_from_team(user_id, team_id):
        user_id = InputValidator.validate_id(user_id)
        team_id = InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        team = Get_Sql.get_sql(
            models.Team,
            team_id=team_id
        )

        if not user:
            raise ValueError("User does not exist.")

        user = user[0]

        if not team:
            raise ValueError("Team does not exist.")

        team = team[0]

        membership = Get_Sql.get_sql(models.TeamMember, user_id=user_id, team_id=team_id)

        if not membership:
            raise ValueError("User is not a member of this team.")

        return query_handling(Delete_Sql.delete_sql, model=models.TeamMember, pk_value={"team_id": team_id, "user_id": user_id})

    @staticmethod
    @transaction
    def assign_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        users = Get_Sql.get_sql(models.User, user_id=user_id)

        if not users:
            raise ValueError("User does not exist.")
        user = users[0]

        if user.is_admin:
            raise ValueError("Admin users cannot be assigned as team leaders.")

        teams = Get_Sql.get_sql(models.Team, team_id=team_id)
        if not teams:
            raise ValueError("Team does not exist.")
        team = teams[0]

        if user.company_id != team.company_id:
            raise ValueError("User and team do not belong to the same company.")

        membership = Get_Sql.get_sql(models.TeamMember, user_id=user_id, team_id=team_id)

        if not membership:
           raise ValueError("User is not a member of this team.")

        if user.led_team_id is not None:
            if user.led_team_id != team_id:
                raise ValueError("User is already the leader of another team.")
            else:
                raise ValueError("User is already the leader of this team.")

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id, led_team_id=team_id)
    

    @staticmethod
    @transaction
    def remove_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        users = Get_Sql.get_sql(models.User, user_id=user_id)
        if not users:
            raise ValueError("User does not exist.")

        user = users[0]

        if user.led_team_id is None:
            raise ValueError("User is not a team leader.")

        if user.led_team_id != team_id:
            raise ValueError("User is not the leader of this team.")

        return query_handling(Update_Sql.update_sql, model=models.User,
                              user_id=user_id, led_team_id=None)


    
    


