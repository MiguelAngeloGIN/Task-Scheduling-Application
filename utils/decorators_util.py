from functools import wraps
from fasthtml import common as c
from database.models import session
from utils.jwt_util import JWTUtils

def admin_required(func):
    '''Avoids repetition of try and excepts when verifying admin on admin routes'''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            payload = JWTUtils.verify_admin(request)
            request.state.admin_payload = payload
            return func(request, *args, **kwargs)

        except ValueError as e:
            return c.RedirectResponse(
                f'/login?message={str(e)}&message_type=error',
                status_code=302
            )

    return wrapper


def transaction(func):
    '''Wraps a function in a database transaction, committing if successful and rolling back on exception.'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result

        except Exception:
            session.rollback()
            raise

    return wrapper