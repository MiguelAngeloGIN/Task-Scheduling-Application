from crud.get_crud import Get_Sql
from database import models
from library.validators import InputValidator


class QueryService:
    @staticmethod
    def get_company_users(admin_id):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(models.User, user_id=admin_id )

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        return Get_Sql.get_sql(models.User, company_id=admin.company_id)


    @staticmethod
    def get_company_user(user_id, company_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(company_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id, company_id=company_id)
   
        if not user:
            raise ValueError("User does not exist in this company.")

        return user[0]

    @staticmethod
    def get_company_teams(admin_id):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(models.User, user_id=admin_id)

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        return Get_Sql.get_sql(models.Team, company_id=admin.company_id)

    @staticmethod
    def get_company_team(team_id, company_id):
        InputValidator.validate_id(team_id)
        InputValidator.validate_id(company_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id, company_id=company_id)

        if not team:
            raise ValueError("Team does not exist in this company.")

        return team[0]

    @staticmethod
    def get_user(user_id):
        InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id)

        if not user:
            raise ValueError("User does not exist.")

        return user[0]

    

    @staticmethod
    def get_user_by_email(email):
        InputValidator.validate_str(email)

        user = Get_Sql.get_sql(models.User, email=email)

        if not user:
            raise ValueError("User does not exist.")

        return user[0]

    @staticmethod
    def get_company(company_id):
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        return company[0]

    @staticmethod
    def get_team(team_id):
        InputValidator.validate_id(team_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id)

        if not team:
            raise ValueError("Team does not exist.")

        return team[0]


    @staticmethod
    def get_invitation(token):
        InputValidator.validate_str(token)

        invitation = Get_Sql.get_sql(models.Invitation, token=token)

        if not invitation:
            raise ValueError("Invitation does not exist.")

        return invitation[0]


    @staticmethod
    def search_user(query, company_id):
        InputValidator.validate_str(query)
        InputValidator.validate_id(company_id)

        return Get_Sql.search_by_company_sql(models.User, company_id, query, "email")
    
    @staticmethod
    def search_team(query, company_id):
        InputValidator.validate_str(query)
        InputValidator.validate_id(company_id)

        return Get_Sql.search_by_company_sql(models.Team, company_id, query, "name")
    