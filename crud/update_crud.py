from database import models

session = models.session

class Update_Sql:

    @staticmethod
    def update_sql(model, **kwargs):
        pk_column = next(iter(model.__table__.primary_key.columns))
        pk_name = pk_column.name
        pk_value = kwargs.pop(pk_name)
        
        instance = session.query(model).filter(pk_column == pk_value).first()
        if not instance:
            raise ValueError(f"{model.__name__} with {pk_name}={pk_value} not found.")

        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
            else:
                raise ValueError(f"{model.__name__} has no attribute '{key}'.")
        print(f"{model.__name__} with {pk_name}={pk_value} updated.")
