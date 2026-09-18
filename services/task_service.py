from datetime import datetime, timezone

from crud.add_crud import Add_Sql
from crud.delete_crud import Delete_Sql
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from database import models
from library.validators import InputValidator
from services.priority_service import PriorityService
from services.query_service import QueryService
from utils.db_query_util import transaction
from utils.dependencies_util import check_circular_dependencies, check_self_dependency


class TaskService:
    validators = {
    "name": InputValidator.validate_name,
    "description": InputValidator.validate_description,
    "importance": InputValidator.validate_importance,
    "deadline": InputValidator.validate_deadline,
    
}
    @staticmethod
    @transaction
    def create_task(name, description, importance, deadline, team_id, objective_id, author_id):

        deadline = datetime.fromisoformat(deadline)

        params = {
            "name": name,
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

        task = Add_Sql.add_task(params["name"], params["description"], "pending", params["importance"], params["deadline"],
                                 team_id, objective_id)

        Add_Sql.add_task_history(action="create", description="Task created", author_id=author_id, task_id=task.task_id)

        return task

    @staticmethod
    @transaction
    def delete_task(task_id, author_id):
        task_id = InputValidator.validate_id(task_id)
        Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        Delete_Sql.delete_sql(models.Task, task_id)

        Add_Sql.add_task_history(action="delete", description="Task deleted", author_id=author_id, task_id=task_id)

        return True

    @staticmethod
    @transaction
    def update_task(task_id, **kwargs):
        task_id = InputValidator.validate_id(task_id)
        old_task = Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        updates = {}


        for key, value in kwargs.items():
            
            if key not in TaskService.validators:
                raise ValueError(f"Cannot update field: {key}")

            if key == "deadline":
                value = datetime.fromisoformat(value)
            new_value = TaskService.validators[key](value)

            if getattr(old_task, key) != new_value:
                updates[key] = new_value

        if updates:
            Update_Sql.update_sql(models.Task, task_id = task_id, **updates)        
            return True

        raise ValueError("No updates provided.")

    @staticmethod
    @transaction
    def add_dependencies(dependant_id, dependency_ids):
        dependant_id = InputValidator.validate_id(dependant_id)

        dependency_ids = [InputValidator.validate_id(dep_id)
                          for dep_id in dependency_ids]

        dependant_task = Get_Sql.get_sql(models.Task, task_id=dependant_id)[0]


        dependencies = QueryService.get_dependencies_by_objective(dependant_task.objective_id)

        task_graph = {}
  
        for dep in dependencies:
            task_graph.setdefault(dep.dependant, []).append(dep.dependency)


        for dependency_id in dependency_ids:
            print("single dependency:", dependency_id, type(dependency_id))

            dependency_task = Get_Sql.get_sql(models.Task, task_id=dependency_id)[0]

            check_self_dependency(dependant_id, dependency_id)


            if dependant_task.objective_id != dependency_task.objective_id:
                raise ValueError("Tasks must belong to the same objective.")

            task_graph.setdefault(dependant_id, []).append(dependency_id)


        result = check_circular_dependencies(task_graph)
        if result["has_cycle"]:
            raise ValueError(f"Circular dependency detected: {result['cycle']}")


        for dependency_id in dependency_ids:
            Add_Sql.add_dependency(dependant_id, dependency_id)

        return True


    @staticmethod
    @transaction
    def remove_dependencies(task_id, dependency_ids_pk):

        task_id = InputValidator.validate_id(task_id)

        dependency_ids_pk = [InputValidator.validate_id(dep_pk)
                             for dep_pk in dependency_ids_pk]

        old_dependencies = []

        for dep_pk in dependency_ids_pk:

            dep_row = Get_Sql.get_sql(models.Dependency, dependency_id=dep_pk)

            if not dep_row:
                raise ValueError("Dependency not found.")

            dep_row = dep_row[0]

            if dep_row.dependant != task_id:
                raise ValueError("Selected dependency does not belong to this task.")

            old_dependencies.append(dep_row.dependency)

        for dep_pk in dependency_ids_pk:
            Delete_Sql.delete_sql(models.Dependency, dep_pk)

        return True


    @staticmethod
    @transaction
    def complete_task(task_id, author_id):

        task_id = InputValidator.validate_id(task_id)
        tasks = Get_Sql.get_sql(models.Task, task_id=task_id)
        if not tasks:
            raise ValueError("Task not found.")
        task = tasks[0]

        if task.status == "completed":
            raise ValueError("Task already completed.")

        Update_Sql.update_sql(models.Task, task_id=task_id,status="completed")

        Delete_Sql.delete_dependencies_by_task(task_id)

        Add_Sql.add_task_history(action="complete",description="Task completed",
                                  author_id=author_id,task_id=task_id)

        return True

    

    @staticmethod
    def get_sorted_tasks_by_objective(objective_id): # still gotta check it later
        objective_id = InputValidator.validate_id(objective_id)
        tasks = Get_Sql.get_sql(models.Task, objective_id=objective_id)

        if not tasks:
            raise ValueError("No tasks found.")

        # getting max and min values to normalizedeadline
        deadlines = []
        date_now = datetime.now(timezone.utc).replace(tzinfo=None)

        for task in tasks:
            deadlines.append(task.deadline)

        deadline_differences = [] # convert deadlines to time differences from now 
        for d in deadlines:
         dif = d - date_now
         deadline_differences.append(dif)

        max_deadline = max(deadline_differences) 
        min_deadline = min(deadline_differences)

        prioritized_tasks= []

        for task in tasks:
            deadline = (task.deadline - date_now) # convert deadline to time difference from now to normalize it
            importance = task.importance
          

            priority = PriorityService.calculate_priority(deadline, importance, max_deadline, min_deadline )

            task.priority_score = priority
            prioritized_tasks.append(task)


        sorted_tasks_by_priority = PriorityService.sort_tasks_by_priority(prioritized_tasks)

        dependencies = QueryService.get_dependencies_by_objective(objective_id)

        sorted_tasks = PriorityService.apply_dependency_order(sorted_tasks_by_priority, dependencies)

        return sorted_tasks
    

    

    
