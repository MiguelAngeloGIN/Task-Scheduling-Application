from functools import wraps

from fasthtml import common as c

from services.query_service import QueryService
from utils.jwt_util import JWTUtils


def admin_required(func):
    '''Avoids repetition of try and excepts when verifying admin on admin routes.'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            payload = JWTUtils.verify_admin(request)
            request.state.admin_payload = payload

            return func(request, *args, **kwargs)

        except (ValueError, PermissionError) as e:
            return c.RedirectResponse(
                f'/auth/login?message={str(e)}&message_type=error',
                status_code=302
            )

    return wrapper


def leader_required(func):
    '''Ensures that the user is a team leader.'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.cookies.get("jwt_token")
            payload = JWTUtils.verify_jwt(token)

            request.state.user_payload = payload

            user_id = int(payload["sub"])

            if not QueryService.is_team_leader(user_id):
                raise PermissionError("Leader access required.")

            request.state.user = QueryService.get_user(user_id)

            return func(request, *args, **kwargs)

        except (ValueError, PermissionError) as e:
            return c.RedirectResponse(
                f'/auth/login?message={str(e)}&message_type=error',
                status_code=302
            )

    return wrapper


def leader_or_admin_required(func):
    '''Ensures that the user is either a team leader or an admin.'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.cookies.get("jwt_token")
            payload = JWTUtils.verify_jwt(token)

            request.state.user_payload = payload

            user_id = int(payload["sub"])
            user = QueryService.get_user(user_id)

            if not user.is_admin and not QueryService.is_team_leader(user_id):
                raise PermissionError("Leader or admin access required.")

            request.state.user = user

            return func(request, *args, **kwargs)

        except (ValueError, PermissionError) as e:
            return c.RedirectResponse(
                f'/auth/login?message={str(e)}&message_type=error',
                status_code=302
            )

    return wrapper



def auth_required(func):
    '''Ensures that the user has a valid JWT session.'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            token = request.cookies.get("jwt_token")
            payload = JWTUtils.verify_jwt(token)

            request.state.user_payload = payload

            return func(request, *args, **kwargs)

        except ValueError as e:
            return c.RedirectResponse(
                f'/auth/login?message={str(e)}&message_type=error',
                status_code=302
            )

    return wrapper

