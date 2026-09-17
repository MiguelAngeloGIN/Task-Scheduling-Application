from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.add_crud import Add_Sql
from crud.delete_crud import Delete_Sql
from database import models
from utils.db_query_util import query_handling
import secrets
from library.validators import InputValidator
from datetime import datetime, timedelta, timezone
from services.email_service import EmailService
from utils.db_query_util import transaction


class CompanyService:

    @staticmethod
    def add_user_to_company(user_id, company_id):
        user_id = InputValidator.validate_id(user_id)
        company_id = InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        users = Get_Sql.get_sql(models.User, user_id=user_id
        )
        user = users[0] if users else None

        if not user:
            raise ValueError("User does not exist.")

        if user.company_id is not None:
            raise ValueError("User already belongs to a company.")

        query_handling(Update_Sql.update_sql, model=models.User, user_id=user.user_id, company_id=company_id)


    @staticmethod
    def delete_invitation(token):
        return query_handling(Delete_Sql.delete_sql, model=models.Invitation, token=token)


    @staticmethod
    @transaction
    def create_company(name, user_id):
        InputValidator.validate_name(name)
        user_id = InputValidator.validate_id(user_id)

        users = Get_Sql.get_sql (models.User, user_id=user_id)
        if not users:
            raise ValueError("User is not registered.")
        user = users[0]

        if user.company_id is not None:
            raise ValueError("User already belongs to a company.")

        company =query_handling(Add_Sql.add_company, name=name, error="Company name already exists.")

        CompanyService.add_user_to_company(user_id=user_id, company_id=company.company_id)
        return company



    @staticmethod
    @transaction
    def accept_invitation(user_id, company_id, token): 
        user_id = InputValidator.validate_id(user_id)
        company_id = InputValidator.validate_id(company_id)

        invitation = Get_Sql.get_sql(models.Invitation,token=token)

        if not invitation:
            raise ValueError("Invitation does not exist or has expired.")

        invitation = invitation[0]

        if invitation.company_id != company_id:
            raise ValueError("Invitation does not belong to this company.")
        users = Get_Sql.get_sql(models.User, user_id=user_id)

        if not users:
            raise ValueError("User does not exist.")

        user = users[0]

        if invitation.invited_email != user.email:
            raise ValueError("Invitation email does not match user email.")

        CompanyService.add_user_to_company(user_id=user_id, company_id=company_id)

        query_handling(Delete_Sql.delete_sql, model=models.Invitation, token=token)
        return True

   
    @staticmethod
    @transaction
    def create_invitation(invited_email, company_id, invited_by):
        InputValidator.validate_email(invited_email)
        InputValidator.validate_id(company_id)
        InputValidator.validate_id(invited_by)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        admin = Get_Sql.get_sql(models.User, user_id=invited_by)

        if not admin:
            raise ValueError("Inviting user does not exist.")

        admin = admin[0]

        if admin.company_id != company_id:
            raise ValueError("Admin does not belong to this company.")

        invited_users = Get_Sql.get_sql(models.User, email=invited_email)

        if not invited_users:
            raise ValueError("User with this email does not exist.")

        invited_user = invited_users[0]

        if invited_user.company_id == company_id:
            raise ValueError("User is already in this company.")

        
        if invited_user.company_id is not None:
            raise ValueError("User already belongs to another company.")

        existing_invitation = Get_Sql.get_sql(models.Invitation, invited_email=invited_user.email, company_id=company_id)
        expiry = existing_invitation[0].expires_at if existing_invitation else None

        if expiry:
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)

            if expiry > datetime.now(timezone.utc):
                raise ValueError("This user is already invited to this company.")

            if expiry <= datetime.now(timezone.utc):
                query_handling(Delete_Sql.delete_sql, model=models.Invitation, token=existing_invitation[0].token)

        token = secrets.token_urlsafe(32)

        expiration_time = (
            datetime.now(timezone.utc) + timedelta(days=3)
        )

        invitation_link = (
            f"http://localhost:5001/accept-invitation?token={token}"
        )

        query_handling(Add_Sql.add_invitation, company_id=company_id, invited_email=invited_user.email, invited_by=invited_by,
                        token=token, expires_at=expiration_time, error="Failed to create invitation.")

        EmailService.send_invitation_email(invited_email=invited_user.email, invitation_link=invitation_link, company_name=company[0].name)

        return invitation_link

        

    @staticmethod
    @transaction
    def remove_user_from_company(user_id):
        user_id = InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id)

        if not user:
            raise ValueError("User does not exist.")

        return query_handling(Update_Sql.update_sql, model=models.User, user_id=user_id, company_id=None
        )

    