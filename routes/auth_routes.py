from services.auth_service import AuthService
from typing import Optional
from components.auth_components import Pages
from fasthtml import common as c
from core.app import rt
from utils.jwt_util import JWTUtils


@rt('/auth/signup', methods=['GET'])
def get_signup():
    return Pages.signup_page()

    
@rt('/auth/signup', methods=['POST'])
def post_signup(first_name: str, last_name: str, email: str, password: str):
   
    try:
        AuthService.sign_up(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        return c.RedirectResponse('/auth/login?message=Account created successfully&message_type=success', status_code=302)
    
    except ValueError as e:
        return Pages.signup_page(
            message=str(e),
            message_type="error",
            first_name=first_name,
            last_name=last_name,
            email=email
        )

@rt('/auth/admin-signup', methods=['GET'])
def get_admin_signup():
    return Pages.signup_page(action='/auth/admin-signup')

@rt('/auth/admin-signup', methods=['POST'])
def post_admin_signup(first_name: str, last_name: str,
                        email: str, password: str):
    try:
        user = AuthService.sign_up(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_admin=True
        )

        token = AuthService.generate_jwt(user)

        response = c.RedirectResponse( '/admin/company/create', status_code=302)
        response.set_cookie("jwt_token", token, httponly=True, secure=False, samesite='lax', max_age=24*60*60) 
        return response

    except ValueError as e:
        return Pages.signup_page(action='/auth/admin-signup',
            message=str(e),
            message_type="error",
            first_name=first_name,
            last_name=last_name,
            email=email
        )



    


@rt('/auth/login', methods=['GET'])
def get_login(message: Optional[str] = None, message_type: Optional[str] = None):
     return Pages.login_page(message=message, message_type=message_type)


@rt('/auth/login', methods=['POST'])
def post_login(email: str, password: str):
    try:
        token = AuthService.login(email=email, password=password)

        payload = JWTUtils.decode_jwt(token)

        if payload['admin']:
            response = c.RedirectResponse('/admin-dashboard?message=Logged in successfully&message_type=success', status_code=302)

        else:
            response = c.RedirectResponse('/dashboard?message=Logged in successfully&message_type=success', status_code=302)
            
        response.set_cookie("jwt_token", token, httponly=True, secure=False, samesite='lax', max_age=24*60*60) 
        ## secure = False to allow testing on localhost, should be True in production with HTTPS
        return response
    
    except ValueError as e:
        return Pages.login_page(
            message=str(e),
            message_type="error",
            email=email
        )

    
@rt('/auth/logout', methods=['POST'])
def post_logout():
    response = c.RedirectResponse('/auth/login?message=Logged out&message_type=success', status_code=302)
    response.delete_cookie("jwt_token")
    return response


@rt('/auth/reset-password', methods = ['GET'])
def get_password_reset():
    return Pages.reset_password_page()

@rt('/auth/reset-password', methods = ['POST'])
def post_password_reset(email: str):
    try:
        AuthService.create_password_reset(email=email)
        return Pages.reset_email_sent_page()
    except ValueError as e:
        return Pages.reset_password_page(message=str(e), message_type="error")


@rt('/auth/new-password', methods = ['GET'])
def get_new_password(message: Optional[str] = None, message_type: Optional[str] = None, token: str = ''):
    try:
        AuthService.verify_reset_token(token=token)
        return Pages.new_password_page(message=message, message_type=message_type, token=token)
    except ValueError as e:
        return Pages.invalid_token_page(message=str(e), message_type="error")

@rt('/auth/new-password', methods = ['POST'])
def post_new_password(token: str, new_password: str, confirm_password: str):
    try:
        if new_password != confirm_password:
            raise ValueError("The passwords do not match.")

        AuthService.reset_password(token=token, new_password=new_password)
        return c.RedirectResponse('/auth/login?message=Password reset successfully&message_type=success', status_code=302)
    except ValueError as e:
        if "token" in str(e).lower():
            return Pages.invalid_token_page(message=str(e), message_type="error")
        return Pages.new_password_page(message=str(e), message_type="error", token=token)

