from functools import wraps

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database import models
from database.models import session


def query_handling(func, *args, error=None, **kwargs):
    ''' An utility function to handle database queries and exceptions. '''
    try:
        return func(*args, **kwargs)

    except IntegrityError as e:
        models.session.rollback()

        if error:
            raise ValueError(error) from e

        raise

    except SQLAlchemyError as e:
        models.session.rollback()
        raise ValueError("Database error.") from e


def transaction(func):
    '''Wraps a function in a database transaction, committing if everything is successful and rolling back on exception.'''
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result


        except SQLAlchemyError as e:
            session.rollback()
            raise ValueError("Database error.") from e

        except Exception:
            session.rollback()
            raise

    return wrapper