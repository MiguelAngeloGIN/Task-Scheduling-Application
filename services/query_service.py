from crud.get_crud import Get_Sql
from database import models
from library.validators import InputValidator


class QueryService:
    @staticmethod
    def get_company_users(admin_id):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(models.User, user_id=admin_id )

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        return Get_Sql.get_sql(models.User, company_id=admin.company_id)


    @staticmethod
    def get_company_user(user_id, company_id):
        InputValidator.validate_id(user_id)
        InputValidator.validate_id(company_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id, company_id=company_id)
   
        if not user:
            raise ValueError("User does not exist in this company.")

        return user[0]

    @staticmethod
    def get_company_teams(admin_id, query=None):
        InputValidator.validate_id(admin_id)

        admin = Get_Sql.get_sql(models.User, user_id=admin_id)

        if not admin:
            raise ValueError("Admin does not exist.")

        admin = admin[0]

        if admin.company_id is None:
            raise ValueError("Admin does not belong to a company.")

        filters = [models.Team.company_id == admin.company_id]
        if query:
            filters.append(models.Team.name.ilike(f"%{query}%"))

        return Get_Sql.get_sql(models.Team, *filters)

    @staticmethod
    def get_company_team(team_id, company_id):
        InputValidator.validate_id(team_id)
        InputValidator.validate_id(company_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id, company_id=company_id)

        if not team:
            raise ValueError("Team does not exist in this company.")

        return team[0]

    @staticmethod
    def get_user(user_id):
        InputValidator.validate_id(user_id)

        user = Get_Sql.get_sql(models.User, user_id=user_id)

        if not user:
            raise ValueError("User does not exist.")

        return user[0]

    @staticmethod
    def get_task(task_id):
        InputValidator.validate_id(task_id)

        task = Get_Sql.get_sql(models.Task, task_id=task_id)

        if not task:
            raise ValueError("Task does not exist.")

        return task[0]

    

    @staticmethod
    def get_user_by_email(email):
        InputValidator.validate_str(email)

        user = Get_Sql.get_sql(models.User, email=email)

        if not user:
            raise ValueError("User does not exist.")

        return user[0]

    @staticmethod
    def get_company(company_id):
        InputValidator.validate_id(company_id)

        company = Get_Sql.get_sql(models.Company, company_id=company_id)

        if not company:
            raise ValueError("Company does not exist.")

        return company[0]

    @staticmethod
    def get_team(team_id):
        InputValidator.validate_id(team_id)

        team = Get_Sql.get_sql(models.Team, team_id=team_id)

        if not team:
            raise ValueError("Team does not exist.")

        return team[0]

    @staticmethod
    def get_team_by_leader(leader_id):
        InputValidator.validate_id(leader_id)

        users = Get_Sql.get_sql(models.User, user_id=leader_id)

        if not users:
            raise ValueError("User does not exist.")

        user = users[0]

        if user.led_team_id is None:
            raise ValueError("User is not a team leader.")

        return Get_Sql.get_sql(models.Team, team_id=user.led_team_id)[0]


    @staticmethod
    def get_invitation(token):
        InputValidator.validate_str(token)

        invitation = Get_Sql.get_sql(models.Invitation, token=token)

        if not invitation:
            raise ValueError("Invitation does not exist.")

        return invitation[0]

    @staticmethod
    def get_objective(objective_id):
        InputValidator.validate_id(objective_id)

        objective = Get_Sql.get_sql(models.Objective, objective_id=objective_id)

        if not objective:
            raise ValueError("Objective does not exist.")

        return objective[0]

    @staticmethod
    def get_objectives_by_company(company_id, query=None):
        InputValidator.validate_id(company_id)

        filters = [models.Objective.progress != 100,
                   models.Objective.is_archived == False,
                   models.Objective.company_id == company_id
                   ]

        if query:
            filters.append(
                models.Objective.name.like(f"%{query}%")
            )

        objectives = Get_Sql.get_sql(models.Objective, *filters)

        if not objectives:
            raise ValueError("No objectives found for this company.")

        return objectives

    @staticmethod
    def get_objective_by_task(task_id):
        InputValidator.validate_id(task_id)

        tasks = Get_Sql.get_sql(models.Task, task_id=task_id)

        if not tasks:
            raise ValueError("Task does not exist.")

        task = tasks[0]

        if not task.objective:
            raise ValueError("Objective does not exist.")

        return task.objective

    @staticmethod
    def get_tasks_by_objective(objective_id, company_id):
        InputValidator.validate_id(objective_id)
        InputValidator.validate_id(company_id)

        objective = Get_Sql.get_sql(models.Objective, objective_id=objective_id,
                                    company_id=company_id
                                    )

        if not objective:
            raise ValueError("Objective not found.")

        tasks = Get_Sql.get_sql(models.Task, models.Task.status!="completed", objective_id=objective_id)

        if not tasks:
            raise ValueError("No tasks found for this objective.")

        return tasks

    @staticmethod
    def get_tasks_by_team_leader(leader_id, query=None):
        InputValidator.validate_id(leader_id)

        users = Get_Sql.get_sql(models.User, user_id=leader_id)

        if not users:
            raise ValueError("User does not exist.")

        team_id = users[0].led_team_id

        if not team_id:
            raise ValueError("Team not found.")

        
        filters = [models.Task.status != "completed",
                   models.Task.team_id == team_id
                   ]

        if query:
            filters.append(
            models.Task.name.like(f"%{query}%")
        )

        tasks = Get_Sql.get_sql(models.Task, *filters)

        if not tasks:
            raise ValueError("No tasks found for this team.")

        return tasks
    

    @staticmethod
    def is_team_leader(user_id):
        InputValidator.validate_id(user_id)

        users = Get_Sql.get_sql(models.User, user_id=user_id)

        if not users:
            raise ValueError("User does not exist.")

        user = users[0]

        return user.led_team_id is not None


    @staticmethod
    def search_user(query, company_id):
        InputValidator.validate_str(query)
        InputValidator.validate_id(company_id)

        return Get_Sql.search_by_company_sql(models.User, company_id, query, "email")
    
    @staticmethod
    def search_team(query, company_id):
        InputValidator.validate_str(query)
        InputValidator.validate_id(company_id)

        return Get_Sql.search_by_company_sql(models.Team, company_id, query, "name")

    @staticmethod
    def search_all_users(query, exclude_user_id=None):
        InputValidator.validate_str(query)

        return Get_Sql.search_all_users(query, exclude_user_id=exclude_user_id)

    
    @staticmethod
    def get_tasks_for_dependency(task_id, query=None):
        task = Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        filters = [
        models.Task.objective_id == task.objective_id,
        models.Task.task_id != task_id,
        models.Task.status != "completed"
    ]

        if query:
            filters.append(models.Task.name.like(f"%{query}%") )

        return Get_Sql.get_sql(models.Task, *filters)


    @staticmethod
    def get_dependencies_by_objective(objective_id):

        return (models.session.query(models.Dependency)
        .join(
            models.Task,
            models.Dependency.dependant == models.Task.task_id
        )
        .filter(
            models.Task.objective_id == objective_id
        )
        .all()
    )


    @staticmethod
    def get_tasks_by_user(user_id, query=None):
        InputValidator.validate_id(user_id)

        team_memberships = Get_Sql.get_sql(models.TeamMember, 
                                           user_id=user_id)

        if not team_memberships:
            raise ValueError("User is not part of any team.")

        team_ids = [membership.team_id 
                    for membership in team_memberships]

        filters = [models.Task.team_id.in_(team_ids), 
                   models.Task.status != "completed"]

        if query:
            filters.append(models.Task.name.like(f"%{query}%"))

        tasks = Get_Sql.get_sql(models.Task, *filters)

        if not tasks:
            raise ValueError("No available tasks found.")

        return tasks

    @staticmethod
    def get_dependencies_by_task(task_id, query=None):

        InputValidator.validate_id(task_id)

        query_db = (models.session.query(models.Dependency)
        .join(
            models.Task,
            models.Dependency.dependency == models.Task.task_id
        )
        .filter(models.Dependency.dependant == task_id)
      )

        if query:
            query_db = query_db.filter(
            models.Task.name.like(f"%{query}%")
        )

        return query_db.all()




