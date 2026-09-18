from database import models

session = models.session

class Delete_Sql:
    @staticmethod
    def delete_sql(model, pk_value=None, token=None):
        '''Generic delete method'''
        if token:
            instance = session.query(model).filter_by(token=token).first()

        elif isinstance(pk_value, dict):
            instance = session.query(model).filter_by(**pk_value).first()

        else:
            pk_column = next(iter(model.__table__.primary_key.columns))
            instance = session.query(model).filter(pk_column == pk_value).first()

        if not instance:
            raise ValueError("Instance not found")

        session.delete(instance)
        return f"{model.__name__} deleted."


    @staticmethod
    def delete_dependencies_by_task(task_id): 
        dependencies = session.query(models.Dependency).filter(
            (models.Dependency.dependant == task_id) |
            (models.Dependency.dependency == task_id)
        ).all()

        for dependency in dependencies:
            session.delete(dependency)
