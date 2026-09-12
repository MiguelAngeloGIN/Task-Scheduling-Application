from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from database import models

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