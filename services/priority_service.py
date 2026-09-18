
class PriorityService:
    """
    Provides priority calculation and sorting utilities for task scheduling.
    
    Priority is computed using a weighted model:
        - Deadline (50%): Earlier deadlines increase urgency.
        - Importance (50%): User-defined importance (1 - 5).
        - Dependencies: Ensures tasks are scheduled after their dependencies.
    """

    @staticmethod
    def calculate_priority(deadline, importance, max_deadline, min_deadline):
        """
        Calculate a normalized weighted priority score for a task between 0 and 1.

        Args:
            deadline (float): Numeric representation of the task deadline.
            importance (int): Importance level (1 - 5).
            max_deadline (float): Latest deadline among all tasks.
            min_deadline (float): Earliest deadline among all tasks.

        Returns:
            float: Priority score between 0 and 1.
        """

       
        if max_deadline == min_deadline:
            normalized_deadline = 1
        else:
            normalized_deadline = 1 - (deadline - min_deadline)/ (max_deadline - min_deadline)

        normalized_importance = (importance - 1) / 4 


        # Calculate the weighted priority score
        priority_score = (0.5 * normalized_deadline) + (0.5 * normalized_importance)
        return priority_score
 
    @staticmethod
    def sort_tasks_by_priority(tasks):
        if not tasks:
            return []
    
        return sorted(
        tasks, 
        key=lambda task: task.priority_score, 
        reverse=True
    )

    @staticmethod
    def apply_dependency_order(sorted_tasks, dependencies):
        """
        DFS-based reorder of tasks based on dependencies, ensuring that dependent tasks come after their dependencies.

        Args:
            sorted_tasks (list): List of tasks sorted by priority.
            dependencies (list): List of dependency relationships, each represented as an object with 'dependant' and 'dependency' attributes.

        Returns:
            list: Reordered list of tasks respecting dependencies.
        """

        task_dict = {task.task_id: task for task in sorted_tasks}
        ordered_tasks = []
        visited = set()

        def visit(task_id):
            if task_id in visited:
                return
            visited.add(task_id)
            for dep in dependencies:
                if dep.dependant == task_id:
                    visit(dep.dependency)
            if task_id in task_dict:
                ordered_tasks.append(task_dict[task_id])

        for task in sorted_tasks:
            visit(task.task_id)

        return ordered_tasks

     