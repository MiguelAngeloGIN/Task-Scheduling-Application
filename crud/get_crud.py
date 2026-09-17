from database import models

session = models.session

class Get_Sql:

    @staticmethod
    def get_sql(model, *filters, **kwargs):
        query = session.query(model)

        for condition in filters:
            query = query.filter(condition)

        for key, value in kwargs.items():
            if hasattr(model, key):
                query = query.filter(getattr(model, key) == value)
            else:
                raise ValueError(f"{model.__name__} has no attribute '{key}'.")
        results = query.all()
        return results




    @staticmethod
    def search_by_company_sql(model, company_id, query, attribute):
        if not hasattr(model, attribute):
            raise ValueError(f"{model.__name__} has no attribute '{attribute}'.")

        return session.query(model).filter(
            getattr(model, "company_id") == company_id,
            getattr(model, attribute).like(f"%{query}%")
        ).all()

    @staticmethod
    def search_all_users(query, exclude_user_id=None):
        users = session.query(models.User).filter(
        models.User.email.like(f"%{query}%")
        )

        if exclude_user_id:
            users = users.filter(
            models.User.user_id != exclude_user_id
        )

        return users.all()
