import jwt, os
from dotenv import load_dotenv
from typing import Optional

load_dotenv() 
secret_key = os.getenv("JWT_SECRET_KEY")

if not secret_key:
    raise ValueError("JWT_SECRET_KEY not found in environment variables")

class JWTUtils:
    @staticmethod
    def generate_jwt(payload):

        token = jwt.encode(payload, secret_key, algorithm="HS256")
        return token

    # to decode the JWT token and verify its validity or get email and user_id from it
    @staticmethod
    def decode_jwt(token):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")


    
    @staticmethod
    def verify_jwt(token: Optional[str]):
        if not token:
            raise ValueError("User not authenticated.")
        payload = JWTUtils.decode_jwt(token)
        return payload

    @staticmethod
    def verify_admin(request):
        token = request.cookies.get("jwt_token")
        payload = JWTUtils.verify_jwt(token)

        if not payload.get("admin"):
            raise PermissionError("Admin access required.")

        return payload