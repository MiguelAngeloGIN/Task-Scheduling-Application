import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()  

   
def send_email(to_email, subject, body, html=False):
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")

        if not email_user or not email_password:
            raise ValueError("EMAIL_USER or EMAIL_PASSWORD not found in environment variables")

        msg = EmailMessage()
        if html:
            msg.add_alternative(body, subtype='html')
        else:
            msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = to_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(msg['From'], email_password)
            server.send_message(msg)
        return

