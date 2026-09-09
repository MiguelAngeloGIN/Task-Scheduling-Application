from library.validators import InputValidator
from crud.add_crud import Add_Sql
from crud.get_crud import Get_Sql
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError    
from datetime import datetime, timezone, timedelta
from utils.jwt_util import JWTUtils
from utils.query_util import query_handling
from database import models



class UserService:
    ph = PasswordHasher()

    @staticmethod
    def add_company(name):
        name = InputValidator.validate_name(name)

        query_handling(Add_Sql.add_company, name, 
                       error="Company with this name already exists.")
        
    @staticmethod
    def add_team(name, company_id):
        name = InputValidator.validate_name(name)
        company_id = InputValidator.validate_id(company_id)

        return query_handling(Add_Sql.add_team, name, company_id, 
                              error="Team with this name already exists.")

    @staticmethod
    def sign_up(first_name, last_name, email, password):
       
        first_name = InputValidator.validate_name(first_name)
        last_name = InputValidator.validate_name(last_name)
        email = InputValidator.validate_email(email)
        password = InputValidator.validate_password(password)

        password_hash = UserService.ph.hash(password)
       
        return query_handling(Add_Sql.add_user, first_name, last_name, email, password_hash,
                              error="User with this email already exists.")


    @staticmethod
    def login(email, password):
        email = InputValidator.validate_email(email)
        password = InputValidator.validate_password(password)

        users = Get_Sql.get_sql(models.User, email=email)
        if not users:
            raise ValueError("User with this email does not exist.")
        user = users[0]
        try:
            UserService.ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise ValueError("Incorrect password.")

        payload = {
            "sub": str(user.user_id),
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=24),  
            "iat": datetime.now(timezone.utc),
            "admin" : user.is_admin,
            "team_leader": user.is_team_leader
        }

        token = JWTUtils.generate_jwt(payload)
        print(f"User {user.user_id} logged in. JWT token generated.")
        return token

        
