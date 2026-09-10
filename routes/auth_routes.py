from services.user_service import UserService
from services.password_reset_service import ResetService
from typing import Optional
from components.auth_components import Pages
from fasthtml import common as c
from core.app import rt


@rt('/signup', methods=['GET'])
def get_signup():
    return Pages.signup_page()

    
@rt('/signup', methods=['POST'])
def post_signup(first_name: str, last_name: str, email: str, password: str):
   
    try:
        UserService().sign_up(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        print("POST /signup triggered")
        return c.RedirectResponse('/login?message=Account created successfully&message_type=success', status_code=302)
    
    except ValueError as e:
        return Pages.signup_page(
            message=str(e),
            message_type="error",
            first_name=first_name,
            last_name=last_name,
            email=email
        )

@rt('/admin-signup', methods=['GET'])
def get_admin_signup():
    return Pages.signup_page(action='/company-signup')

@rt('/company-signup', methods=['POST'])
def post_company_signup(first_name: str, last_name: str,
                        email: str, password: str):
    try:
        user = UserService.sign_up(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_admin=True
        )

        token = UserService.generate_jwt(user)

        response = c.RedirectResponse( '/create-company', status_code=302)
        response.set_cookie("jwt_token", token, httponly=True, secure=False, samesite='lax', max_age=24*60*60) 
        return response

    except ValueError as e:
        return Pages.signup_page(action='/company-signup',
            message=str(e),
            message_type="error",
            first_name=first_name,
            last_name=last_name,
            email=email
        )



    


@rt('/login', methods=['GET'])
def get_login(message: Optional[str] = None, message_type: Optional[str] = None):
     return Pages.login_page(message=message, message_type=message_type)


@rt('/login', methods=['POST'])
def post_login(email: str, password: str):
    try:
        token = UserService().login(email=email, password=password)

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

    
@rt('/logout', methods=['POST'])
def post_logout():
    response = c.RedirectResponse('/login?message=Logged out&message_type=success', status_code=302)
    response.delete_cookie("jwt_token")
    return response


@rt('/reset-password', methods = ['GET'])
def get_password_reset():
    return Pages.reset_password_page()

@rt('/reset-password', methods = ['POST'])
def post_password_reset(email: str):
    try:
        ResetService().create_reset_link(email=email)
        return c.RedirectResponse(f'/paste-token?email={email}&message=Password reset token created and sent to your email&message_type=success', status_code=302)
    except ValueError as e:
        return Pages.reset_password_page(message=str(e), message_type="error")


@rt('/new-password', methods = ['GET'])
def get_new_password(message: Optional[str] = None, message_type: Optional[str] = None, token: str = ''):
    try:
        ResetService.verify_reset_token(token=token)
        return Pages.new_password_page(message=message, message_type=message_type, token=token)
    except ValueError as e:
        return Pages.invalid_token_page(message=str(e), message_type="error")

@rt('/new-password', methods = ['POST'])
def post_new_password(token: str, new_password: str):
    try:
        ResetService().reset_password(token=token, new_password=new_password)
        return c.RedirectResponse('/login?message=Password reset successfully&message_type=success', status_code=302)
    except ValueError as e:
        return Pages.invalid_token_page(message=str(e), message_type="error")

