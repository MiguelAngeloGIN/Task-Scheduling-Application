import secrets
from utils.email_util import EmailSender
from datetime import datetime, timezone, timedelta
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from database import models

class ResetService:
    @staticmethod
    def create_reset_token(email):
        users = Get_Sql.get_sql(models.User, email = email)
        if not users:
            raise ValueError("User with this email does not exist.")
        user = users[0]
        user_id = user.user_id

        if user.reset_token or  user.reset_token_expires_at:

            Update_Sql.update_sql(models.User, user_id = user_id, reset_token = None, reset_token_expires_at = None)
             
        new_token = secrets.token_urlsafe(32)  
        expiry = datetime.now(timezone.utc) + timedelta(minutes=30)

        Update_Sql.update_sql(models.User, user_id = user_id, reset_token = new_token, reset_token_expires_at = expiry)

        try:
            EmailSender.send_email (to_email = email, 
                         subject = "Your password reset token",
                         body = f"Below is your password reset token. It will expire in 30 minutes\n {new_token}")
            return {"success": True, "message": "Reset token sent successfully!"}
        except Exception as e:
            raise ValueError(f"Failed to send reset token: {str(e)}") 

    @staticmethod
    def verify_reset_token(email, token):
        users = Get_Sql.get_sql(models.User, email = email)
        if not users:
            raise ValueError("User not found")
        user = users[0]

        if not user.reset_token or not user.reset_token_expires_at:
            raise ValueError("No reset token found for this user")

        if user.reset_token != token:
            raise ValueError("Invalid reset token")

        if datetime.now(timezone.utc) > user.reset_token_expires_at:
            raise ValueError("Reset token has expired")

        print(f"Reset token verified successfully for user with email: {email}")
        return True


    @staticmethod
    def reset_password(email, token, new_password):
        users = Get_Sql.get_sql(models.User, email = email)
        if not users:
            raise ValueError("User with this email does not exist.")
        user = users[0]
        user_id = user.user_id

        ResetService.verify_reset_token(email, token)

        from library.validators import InputValidator
        from services.user_services import UserService

        InputValidator.validate_password(new_password)
        new_password_hash = UserService.ph.hash(new_password)

        Update_Sql.update_sql(models.User, user_id = user_id, password_hash=new_password_hash,
                               reset_token=None, reset_token_expires_at=None)

        try:
            EmailSender.send_email(to_email=email,
                                   subject="Your password has been reset",
                                   body="Your password has been successfully reset. If you did not initiate this change, please contact support immediately.")
        except Exception as e:
            raise ValueError(f"Failed to send confirmation email: {str(e)}")
        
        print(f"Password reset successfully for user with email: {email}")

        return {"success": True, "message": "Password reset successfully!"}

        

        

        
        
    


      
       
