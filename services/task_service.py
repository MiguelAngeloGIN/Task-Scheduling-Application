from crud.add_crud import Add_Sql
from crud.get_crud import Get_Sql
from crud.update_crud import Update_Sql
from crud.delete_crud import Delete_Sql
from database import models
from utils.dependencies_util import check_circular_dependencies, check_self_dependency
from library.validators import InputValidator
from services.priority_service import PriorityService
from datetime import datetime, timezone

class TaskService:
    validators = {
    "name": InputValidator.validate_name,
    "description": InputValidator.validate_description,
    "importance": InputValidator.validate_importance,
    "deadline": InputValidator.validate_deadline,
    "duration": InputValidator.validate_duration,
    "difficulty": InputValidator.validate_difficulty,
}
    @staticmethod
    def create_task(name, description, importance, deadline, duration, difficulty, team_id, objective_id, author_id):
        params = {
            "name": name,
            "description": description,
            "importance": importance,
            "deadline": deadline,
            "duration": duration,
            "difficulty": difficulty
        }

        for field, validator in TaskService.validators.items():
            params[field] = validator(params[field])
        team_id = InputValidator.validate_id(team_id)
        objective_id = InputValidator.validate_id(objective_id)

        task = Add_Sql.add_task(params["name"], params["description"], "pending", params["importance"], params["deadline"],
                                 params["duration"], params["difficulty"], team_id, objective_id)

        Add_Sql.add_task_history(action="create", description="Task created", old_value=None, new_value=params, author_id=author_id, task_id=task)

        print(f"Task created successfully with ID: {task}")

        return {"message": "Task created successfully", "task_id": task}

    @staticmethod
    def delete_task(task_id):
        task_id = InputValidator.validate_id(task_id)

        Delete_Sql.delete_sql(models.Task, task_id)

        print(f"Task with ID {task_id} deleted successfully.")

        return {"message": "Task deleted successfully", "task_id": task_id}

    @staticmethod
    def update_task(task_id, author_id, update_description, **kwargs):
        task_id = InputValidator.validate_id(task_id)
        old_task = Get_Sql.get_sql(models.Task, task_id=task_id)[0]

        old_values = {}
        new_values = {}


        for key, value in kwargs.items():
            if key in TaskService.validators:
                old_value = getattr(old_task, key)

                kwargs[key] = TaskService.validators[key](value)

                if old_value != kwargs[key]:
                    old_values[key] = old_value  
                    new_values[key] = kwargs[key]

                
        Update_Sql.update_sql(models.Task, task_id = task_id, **kwargs)
        
        if old_values:
            Add_Sql.add_task_history(action="update", description=update_description, old_value=old_values, new_value=new_values, author_id=author_id, task_id=task_id)

        print(f"Task with ID {task_id} updated successfully.")

        return {"message": "Task updated successfully", "task_id": task_id}

    @staticmethod
    def add_dependency(team_id, dependant_id, dependency_ids, description, author_id):
        dependant_id = InputValidator.validate_id(dependant_id)
        dependency_ids = [InputValidator.validate_id(dep_id) for dep_id in dependency_ids]

        dependecies = Get_Sql.get_sql(models.Dependency, team_id=team_id)
        task_graph = {}
        new_value = {"dependant": dependant_id,
            "dependency": dependency_ids}

        for dep in dependecies:
            if dep.dependant not in task_graph:
                task_graph[dep.dependant] = []
            task_graph[dep.dependant].append(dep.dependency)

        for dependency_id in dependency_ids:
            check_self_dependency(dependant_id, dependency_id)
        check_circular_dependencies(task_graph)

        for dependency_id in dependency_ids:
            Add_Sql.add_dependency(dependant_id, dependency_id)
        Add_Sql.add_task_history(action= "add_dependencies", description = description, old_value= None, new_value=new_value,
                                  author_id=author_id, task_id=dependant_id)

        print(f"Dependency added successfully between dependant task {dependant_id} and dependency tasks {dependency_ids}.")

        return {"message": "Dependency added successfully", "dependant_task_id": dependant_id, "dependency_task_ids": dependency_ids}


    @staticmethod
    def delete_dependency (dependency_ids_pk, description, author_id):
        dependency_ids_pk = [InputValidator.validate_id(dep_pk)  for dep_pk in dependency_ids_pk]

        old_dependencies = []
        dependant_id = None

        for dep_pk in dependency_ids_pk:
            dep_row = Get_Sql.get_sql(models.Dependency, dependency_id_pk=dep_pk)[0]
            if dependant_id is None:
                dependant_id = dep_row.dependant
            old_dependencies.append(dep_row.dependency)

        old_value = {
        "dependant": dependant_id,
        "dependency": old_dependencies
        }
        for dep_pk in dependency_ids_pk:
            Delete_Sql.delete_sql(models.Dependency, dep_pk)

        Add_Sql.add_task_history(action="delete_dependencies", description=description, old_value=old_value,
                                 new_value=None, author_id=author_id, task_id=dependant_id)

        return {
            "message": "Dependency deleted successfully",
            "dependant_task_id": dependant_id,
            "dependency_task_ids": old_dependencies
        }

    @staticmethod
    def get_sorted_tasks_by_team(team_id): # still gotta check it later
        team_id = InputValidator.validate_id(team_id)
        tasks = Get_Sql.get_sql(models.Task, team_id=team_id)

        if not tasks:
            raise ValueError("No tasks found.")

        # getting max and min values to normalize duration and deadline
        durations = []
        deadlines = []
        date_now = datetime.now(timezone.utc).replace(tzinfo=None)

        for task in tasks:
            durations.append( task["duration"])
            deadlines.append(task ["deadline"])

        deadline_differences = [] # convert deadlines to time differences from now 
        for d in deadlines:
         dif = d - date_now
         deadline_differences.append(dif)

        max_duration = max(durations)
        min_duration = min(durations)

        max_deadline = max(deadline_differences) 
        min_deadline = min(deadline_differences)

        prioritized_tasks= []

        for task in tasks:
            deadline = (task["deadline"] - date_now) # convert deadline to time difference from now to normalize it
            importance = task["importance"]
            duration = task["duration"]
            difficulty = task["difficulty"]
            difficulty_preference = "easiest"

            priority = PriorityService.calculate_priority(deadline, importance, duration, difficulty, 
                                               min_duration, max_duration, max_deadline, min_deadline, difficulty_preference )

            task["priority_score"] = priority
            prioritized_tasks.append(task)


        sorted_tasks_by_priority = PriorityService.sort_tasks_by_priority(prioritized_tasks)

        dependecies = Get_Sql.get_sql(models.Dependency, team_id=team_id)

        sorted_tasks = PriorityService.apply_dependency_order(sorted_tasks_by_priority, dependecies)


        return sorted_tasks


    
