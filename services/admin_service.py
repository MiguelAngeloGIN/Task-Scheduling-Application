from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.delete_crud import Delete_Sql
from crud.add_crud import Add_Sql
from database import models
from utils.query_util import query_handling
import secrets
from library.validators import InputValidator
from datetime import datetime, timedelta, timezone
from utils.email_util import send_email


class AdminService:

    @staticmethod
    def create_company(name, user_id):
        InputValidator.validate_name(name)
        InputValidator.validate_id(user_id)

        company =query_handling(Add_Sql.add_company, name=name, error="Company name already exists.")
        AdminService.add_user_to_company(user_id=user_id, company_id=company.company_id)
        return company

   
    @staticmethod
    def create_invitation_link(invited_email, company_id, invited_by):
        InputValidator.validate_email(invited_email)
        InputValidator.validate_id(company_id)
        InputValidator.validate_id(invited_by)

        company = Get_Sql.get_sql(
            models.Company,
            company_id=company_id
        )

        if not company:
            raise ValueError("Company does not exist.")

        admin = Get_Sql.get_sql(models.User, user_id=invited_by)

        if not admin:
            raise ValueError("Inviting user does not exist.")

        admin = admin[0]

        if admin.company_id != company_id:
            raise ValueError("Admin does not belong to this company.")

        invited_user = Get_Sql.get_sql(models.User, email=invited_email)

        if not invited_user:
            raise ValueError("User with this email does not exist.")

        invited_user = invited_user[0]

        if invited_user.company_id == company_id:
            raise ValueError("User is already in this company.")

        
        if invited_user.company_id is not None:
            raise ValueError("User already belongs to another company.")

        existing_invitation = Get_Sql.get_sql(
            models.Invitation,
            user_id=invited_user.user_id,
            company_id=company_id
        )

        if existing_invitation:
            raise ValueError("This user is already invited to this company.")

        token = secrets.token_urlsafe(32)

        expiration_time = (
            datetime.now(timezone.utc) + timedelta(days=3)
        )

        invitation_link = (
            f"http://localhost:5001/invite/{token}"
        )

        query_handling(Add_Sql.add_invitation, company_id=company_id, user_id=invited_user.user_id, invited_by=invited_by,
                        token=token, expires_at=expiration_time, error="Failed to create invitation.")

        return invitation_link

    @staticmethod
    def send_invitation_email(
        invited_email,
        invitation_link,
        company_name
    ):
        InputValidator.validate_email(invited_email)

        subject = f"Taski Invitation from {company_name}"

        body = (
            f"Please click the following link to join "
            f"{company_name}: {invitation_link}"
        )

        send_email(to_email=invited_email, subject=subject, body=body)


    @staticmethod
    def add_user_to_company(user_id, company_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        user = Get_Sql.get_sql(models.User, user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id, company_id=company_id)

    @staticmethod
    def delete_user_from_company(user_id):
        InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id)

        if not user:
            raise ValueError("User does not exist.")

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id, company_id=None
        )


    @staticmethod
    def create_team(team_name, company_id):
        InputValidator.validate_name(team_name)
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        return query_handling(
            Add_Sql.add_team,
            team_name,
            company_id,
            error="Team with this name already exists."
        )

    @staticmethod
    def delete_team(team_id):
        InputValidator.validate_id(team_id)

        team = Get_Sql.get_sql(
            models.Team,
            team_id=team_id
        )

        if not team:
            raise ValueError("Team does not exist.")

        return query_handling(
            Delete_Sql.delete_sql,
            model=models.Team,
            team_id=team_id
        )


    @staticmethod
    def add_user_to_team(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        user = user[0]

        team = Get_Sql.get_sql(
            models.Team,
            team_id=team_id
        )

        if not team:
            raise ValueError("Team does not exist.")

        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(
            Update_Sql.update_sql,
            model=models.User,
            user_id=user_id,
            team_id=team_id
        )

    @staticmethod
    def remove_user_from_team(user_id):
        InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        return query_handling(
            Update_Sql.update_sql,
            model=models.User,
            user_id=user_id,
            team_id=None
        )


    @staticmethod
    def assign_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        user = user[0]

        team = Get_Sql.get_sql(
            models.Team,
            team_id=team_id
        )

        if not team:
            raise ValueError("Team does not exist.")

        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(
            Update_Sql.update_sql,
            model=models.User,
            user_id=user_id,
            team_id=team_id,
            is_team_leader=True
        )

    @staticmethod
    def remove_team_leader(user_id, team_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(team_id)

        user = Get_Sql.get_sql(
            models.User,
            user_id=user_id
        )

        if not user:
            raise ValueError("User does not exist.")

        user = user[0]

        team = Get_Sql.get_sql(
            models.Team,
            team_id=team_id
        )

        if not team:
            raise ValueError("Team does not exist.")

        team = team[0]

        if user.company_id != team.company_id:
            raise ValueError(
                "User and team do not belong to the same company."
            )

        return query_handling(
            Update_Sql.update_sql,
            model=models.User,
            user_id=user_id,
            team_id=None,
            is_team_leader=False
        )


    @staticmethod
    def get_company_users(admin_id):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(
            models.User,
            user_id=admin_id
        )

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        return Get_Sql.get_sql(
            models.User,
            company_id=admin.company_id
        )

    @staticmethod
    def get_company_teams(admin_id):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(
            models.User,
            user_id=admin_id
        )

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        return Get_Sql.get_sql(
            models.Team,
            company_id=admin.company_id
        )

