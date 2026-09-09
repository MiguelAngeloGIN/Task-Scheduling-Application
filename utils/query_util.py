from sqlalchemy.exc import IntegrityError
from database import models


def query_handling(func, *args, error=None):
    """
    A utility function to handle database queries and exceptions.
    """
    try:
        return func(*args)

    except IntegrityError as e:
        models.session.rollback()

        if error:
            raise ValueError(error) from e

        raise