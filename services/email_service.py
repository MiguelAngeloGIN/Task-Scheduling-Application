from utils.email_util import send_email
from library.validators import InputValidator

class EmailService:
    @staticmethod
    def send_reset_email(email, reset_link):
        InputValidator.validate_email(email)
        try:
            send_email(to_email = email, 
                        subject = "Your password reset token",
                        body = f"""<html>
                                        <body>
                                            <p>Below is your password reset link. It will expire in 30 minutes</p> <br> <br>
                                            <a href="{reset_link}">{reset_link}</a>
                                        </body>
                                    </html>""", html=True)
        except Exception as e:
            raise ValueError(f"Failed to send reset token: {str(e)}") 


    @staticmethod
    def send_reset_confirmation_email(email):
        InputValidator.validate_email(email)
        try:
            send_email(to_email=email,
                                       subject="Your password has been reset",
                                       body="Your password has been successfully reset. " \
                                       "If you did not initiate this change, please contact support immediately.")
        except Exception as e:
            raise ValueError(f"Failed to send confirmation email: {str(e)}")
            
    

    @staticmethod
    def send_invitation_email(
        invited_email,
        invitation_link,
        company_name
    ):
        InputValidator.validate_email(invited_email)

        subject = f"Invitation from {company_name}"

        body = (f"""
        <html>
            <body>
                <h1>You're Invited to Join {company_name}</h1>
                <p>Please click the following link to join 
                <br> <br>
                <a href="{invitation_link}">{invitation_link}</a></p>
            </body>
        </html>""")
        try:
            send_email(to_email=invited_email, subject=subject, body=body, html=True)
        except Exception as e:
            raise ValueError(f"Failed to send invitation email: {str(e)}")

    