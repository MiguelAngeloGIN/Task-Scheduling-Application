from library.validators import InputValidator
from crud.add_crud import Add_Sql
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError   
import secrets
from services.email_service import EmailService
from datetime import datetime, timezone, timedelta
from utils.jwt_util import JWTUtils
from utils.query_util import query_handling
from database import models



class AuthService:
    ph = PasswordHasher()

    @staticmethod
    def sign_up(first_name, last_name, email, password, is_admin=False):
       
        first_name = InputValidator.validate_name(first_name)
        last_name = InputValidator.validate_name(last_name)
        email = InputValidator.validate_email(email)
        password = InputValidator.validate_password(password)

        password_hash = AuthService.ph.hash(password)
       
        return query_handling(Add_Sql.add_user, first_name = first_name, last_name=last_name, email=email, password_hash=password_hash, is_admin=is_admin,
                              error="User with this email already exists.")


    @staticmethod
    def generate_jwt(user):
        payload = {
            "sub": str(user.user_id),
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),  
            "iat": datetime.now(timezone.utc),
            "admin" : user.is_admin,
            "team_leader": user.is_team_leader
        }
        return JWTUtils.generate_jwt(payload)
    
    @staticmethod
    def login(email, password):
        email = InputValidator.validate_email(email)

        users = Get_Sql.get_sql(models.User, email=email)
        if not users:
            raise ValueError("Incorrect email or password!")
        user = users[0]
        try:
            AuthService.ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise ValueError("Incorrect email or password!")

        token = AuthService.generate_jwt(user)
        return token



    @staticmethod
    def create_password_reset(email):
        email = InputValidator.validate_email(email)
        users = Get_Sql.get_sql(models.User, email = email)
        if not users:
            raise ValueError("User with this email does not exist.")
        user = users[0]
        user_id = user.user_id
    
        if user.reset_token:
            query_handling(Update_Sql.update_sql, models.User, user_id = user_id, reset_token = None, reset_token_expires_at = None)
                 
        new_token = secrets.token_urlsafe(32)  
        expiry = datetime.now(timezone.utc) + timedelta(minutes=30)
    
        query_handling(Update_Sql.update_sql, models.User, user_id = user_id, reset_token = new_token, reset_token_expires_at = expiry)
        
        reset_link = f"http://localhost:5001/new-password?token={new_token}"
        EmailService.send_reset_email(email, reset_link)
        return reset_link

    
    @staticmethod
    def verify_reset_token(token):
        token = InputValidator.validate_str(token)
        users = Get_Sql.get_sql(models.User, reset_token = token)
        if not users:
            raise ValueError("Invalid or expired reset token.")
        user = users[0]

        if not user.reset_token or not user.reset_token_expires_at:
            raise ValueError("No reset token found for this user")

        expiry = user.reset_token_expires_at

        if expiry.tzinfo is None:
            expiry = expiry.replace(tzinfo=timezone.utc)
    
    
        if datetime.now(timezone.utc) > expiry:
            query_handling(Update_Sql.update_sql, models.User, user_id = user.user_id, reset_token = None, reset_token_expires_at = None)
            raise ValueError("Reset token has expired")
    
        return user
    
    
    @staticmethod
    def reset_password(token, new_password):
        token = InputValidator.validate_str(token)
        user = AuthService.verify_reset_token(token)
        user_id = user.user_id
        email = user.email
    
        InputValidator.validate_password(new_password)
        new_password_hash = AuthService.ph.hash(new_password)
    
        query_handling(Update_Sql.update_sql, models.User, user_id = user_id, password_hash=new_password_hash,
                           reset_token=None, reset_token_expires_at=None)

        try:
            EmailService.send_reset_confirmation_email(email)
        except Exception as e:
            print(f"Failed to send confirmation email: {e}")



    
    

        
