import secrets
from utils.email_util import send_email
from datetime import datetime, timezone, timedelta
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from database import models
from library.validators import InputValidator
from utils.query_util import query_handling
from argon2 import PasswordHasher


class ResetService:
    ph = PasswordHasher()
    @staticmethod
    def create_reset_link(email):
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

        try:
            send_email(to_email = email, 
                         subject = "Your password reset token",
                         body = f"""<html>
                                       <body>
                                          <p>Below is your password reset link. It will expire in 30 minutes</p> <br> <br>
                                          <a href="{reset_link}">{reset_link}</a>
                                       </body>
                                    </html>""", html=True)
            
            return {"success": True, "message": "Reset token sent successfully!"}
        except Exception as e:
            raise ValueError(f"Failed to send reset token: {str(e)}") 

    @staticmethod
    def verify_reset_token(token):
        users = Get_Sql.get_sql(models.User, reset_token = token)
        if not users:
            raise ValueError("Invalid or expired reset token.")
        user = users[0]
        
        if not user.reset_token or not user.reset_token_expires_at:
            raise ValueError("No reset token found for this user")


        if datetime.now(timezone.utc) > user.reset_token_expires_at:
            query_handling(Update_Sql.update_sql, models.User, user_id = user.user_id, reset_token = None, reset_token_expires_at = None)
            raise ValueError("Reset token has expired")

        return user


    @staticmethod
    def reset_password(token, new_password):
        user = ResetService.verify_reset_token(token)
        user_id = user.user_id
        email = user.email

        InputValidator.validate_password(new_password)
        new_password_hash = ResetService.ph.hash(new_password)

        query_handling(Update_Sql.update_sql, models.User, user_id = user_id, password_hash=new_password_hash,
                       reset_token=None, reset_token_expires_at=None)

        try:
            send_email(to_email=email,
                                   subject="Your password has been reset",
                                   body="Your password has been successfully reset. If you did not initiate this change, please contact support immediately.")
        except Exception as e:
            raise ValueError(f"Failed to send confirmation email: {str(e)}")
        

        return {"success": True, "message": "Password reset successfully!"}

        

        

        
        
    


      
       
