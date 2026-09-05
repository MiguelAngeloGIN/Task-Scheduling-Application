from database import models

session = models.session

class Add_Sql:

    @staticmethod
    def add_company(name):
        new_company = models.Company(name=name)
        session.add(new_company)
        session.commit()

    @staticmethod
    def add_user(first_name, last_name, email, password_hash, company_id, team_id, reset_token=None, reset_token_expires_at=None, is_admin=False):
        new_user = models.User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash,
            company_id=company_id,
            team_id=team_id,
            reset_token=reset_token,
            reset_token_expires_at=reset_token_expires_at,
            is_admin=is_admin
        )
        session.add(new_user)
        session.commit()

    @staticmethod
    def add_team(name, company_id):
        new_team = models.Team(
            name=name,
            company_id=company_id
        )
        session.add(new_team)
        session.commit()

    @staticmethod
    def add_objective(name, description, company_id):
        new_objective = models.Objective(
            name=name,
            description=description,
            company_id=company_id
        )
        session.add(new_objective)
        session.commit()

    @staticmethod
    def add_task(name, description, status, importance, deadline, duration, difficulty, team_id, objective_id):
        new_task = models.Task(
            name=name,
            description=description,
            status=status,
            importance=importance,
            deadline=deadline,
            duration=duration,
            difficulty=difficulty,
            team_id=team_id,
            objective_id=objective_id
        )
        session.add(new_task)
        session.commit()

    @staticmethod
    def add_dependency(dependant_id, dependency_id):
        new_dependency = models.Dependency(
            dependant=dependant_id,
            dependency=dependency_id
        )
        session.add(new_dependency)
        session.commit()

    @staticmethod
    def add_task_history(action, description, old_value, new_value, author_id, task_id):
        new_task_history = models.TaskHistory(
            action=action,
            description=description,
            old_value=old_value,
            new_value=new_value,
            author=author_id,
            task=task_id
        )
        session.add(new_task_history)
        session.commit()