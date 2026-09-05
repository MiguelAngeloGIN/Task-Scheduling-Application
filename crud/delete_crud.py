from database import models

session = models.session

class Delete_Sql:
    @staticmethod
    def delete_sql(model, pk_value):
        pk_column = list(model.__table__.primary_key.columns)[0]
        instance = session.query(model).filter(pk_column == pk_value).first()

        if not instance:
            raise ValueError("Instance not found")

        session.delete(instance)
        session.commit()
        return f"{model.__name__} with {pk_column.name}={pk_value} deleted."