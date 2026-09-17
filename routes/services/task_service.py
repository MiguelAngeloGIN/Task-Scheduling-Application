from crud.add_crud import Add_Sql
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.delete_crud import Delete_Sql
from database import models
from utils.dependencies_util import check_circular_dependencies, check_self_dependency
from library.validators import InputValidator
from services.priority_service import PriorityService
from datetime import datetime, timezone
from services.query_service import QueryService
from utils.db_query_util import transaction

class TaskService:
    validators = {
    "title": InputValidator.validate_name,
    "description": InputValidator.validate_description,
    "importance": InputValidator.validate_importance,
    "deadline": InputValidator.validate_deadline,
}
    @staticmethod
    @transaction
    def create_task(title, description, importance, deadline, team_id, objective_id, author_id):

        deadline = datetime.fromisoformat(deadline)

        params = {
            "title": title,
            "description": description,
            "importance": importance,
            "deadline": deadline,
        }

        for field, validator in TaskService.validators.items():
            params[field] = validator(params[field])
        team_id = InputValidator.validate_id(team_id)
        objective_id = InputValidator.validate_id(objective_id)

        objective = Get_Sql.get_sql(models.Objective, objective_id = objective_id)

        if not objective:
            raise ValueError('Please select a valid objective')

        task = Add_Sql.add_task(params["title"], params["description"], "pending", params["importance"], params["deadline"],
                                 team_id, objective_id)

        Add_Sql.add_task_history(action="create", description="Task created", author_id=author_id, task_id=task.task_id)

        return task

    @staticmethod
    @transaction
    def delete_task(task_id):
        task_id = InputValidator.validate_id(task_id)
        Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        Delete_Sql.delete_sql(models.Task, task_id)

        Add_Sql.add_task_history(action="delete", description="Task deleted", author_id=None, task_id=task_id)

        return True

    @staticmethod
    @transaction
    def update_task(task_id, **kwargs):
        task_id = InputValidator.validate_id(task_id)
        old_task = Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        updates = {}


        for key, value in kwargs.items():
            if key in TaskService.validators:
                
                new_value = TaskService.validators[key](value)

                if getattr(old_task, key) != new_value:

                    updates[key] = new_value

        if updates:
            Update_Sql.update_sql(models.Task, task_id = task_id, **updates)        
    

        return True

    @staticmethod
    @transaction
    def add_dependency(team_id, dependant_id, dependency_ids):
        dependant_id = InputValidator.validate_id(dependant_id)
        dependency_ids = [InputValidator.validate_id(dep_id) for dep_id in dependency_ids]

        dependecies = Get_Sql.get_sql(models.Dependency, dependant = dependant_id)
        task_graph = {}

        for dep in dependecies:
            if dep.dependant not in task_graph:
                task_graph[dep.dependant] = []
            task_graph[dep.dependant].append(dep.dependency)

        for dependency_id in dependency_ids:
            check_self_dependency(dependant_id, dependency_id)

            if dependant_id not in task_graph:
                task_graph[dependant_id] = []
            task_graph[dependant_id].append(dependency_id)

        check_circular_dependencies(task_graph)

        for dependency_id in dependency_ids:
            Add_Sql.add_dependency(dependant_id, dependency_id)

        return True


    @staticmethod
    @transaction
    def delete_dependency (dependency_ids_pk):
        dependency_ids_pk = [InputValidator.validate_id(dep_pk)  for dep_pk in dependency_ids_pk]

        old_dependencies = []
        dependant_id = None

        for dep_pk in dependency_ids_pk:
            dep_row = Get_Sql.get_sql(models.Dependency, dependency_id_pk=dep_pk)[0]
            if dependant_id is None:
                dependant_id = dep_row.dependant
            old_dependencies.append(dep_row.dependency)


        for dep_pk in dependency_ids_pk:
            Delete_Sql.delete_sql(models.Dependency, dep_pk)

        return  True
    

    @staticmethod
    def get_sorted_tasks_by_team(team_id): # still gotta check it later
        team_id = InputValidator.validate_id(team_id)
        tasks = Get_Sql.get_sql(models.Task, team_id=team_id)

        if not tasks:
            raise ValueError("No tasks found.")

        # getting max and min values to normalizedeadline
        deadlines = []
        date_now = datetime.now(timezone.utc).replace(tzinfo=None)

        for task in tasks:
            deadlines.append(task ["deadline"])

        deadline_differences = [] # convert deadlines to time differences from now 
        for d in deadlines:
         dif = d - date_now
         deadline_differences.append(dif)

        max_deadline = max(deadline_differences) 
        min_deadline = min(deadline_differences)

        prioritized_tasks= []

        for task in tasks:
            deadline = (task["deadline"] - date_now) # convert deadline to time difference from now to normalize it
            importance = task["importance"]
          

            priority = PriorityService.calculate_priority(deadline, importance, max_deadline, min_deadline )

            task["priority_score"] = priority
            prioritized_tasks.append(task)


        sorted_tasks_by_priority = PriorityService.sort_tasks_by_priority(prioritized_tasks)

        dependecies = Get_Sql.get_sql(models.Dependency, team_id=team_id)

        sorted_tasks = PriorityService.apply_dependency_order(sorted_tasks_by_priority, dependecies)


        return sorted_tasks
    

    

    
