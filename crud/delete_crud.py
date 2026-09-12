from database import models

session = models.session

class Delete_Sql:
    @staticmethod
    def delete_sql(model, pk_value = None, token = None):
        if token:
            instance = session.query(model).filter_by(token=token).first()
        else:
            pk_column = list(model.__table__.primary_key.columns)[0]
            instance = session.query(model).filter(pk_column == pk_value).first()

        if not instance:
            raise ValueError("Instance not found")

        session.delete(instance)
        return f"{model.__name__} deleted."