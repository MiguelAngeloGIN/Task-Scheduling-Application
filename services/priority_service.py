
class PriorityService:
    """
    Provides priority calculation and sorting utilities for task scheduling.
    
    Priority is computed using a weighted model:
        - Deadline (40%): Earlier deadlines increase urgency.
        - Importance (35%): User-defined importance (1 - 5).
        - Duration (15%): Shorter tasks are prioritized (SJF).
        - Difficulty (10%): User preference for hardest or easiest tasks.
        - Dependencies: Ensures tasks are scheduled after their dependencies.
    """

    @staticmethod
    def calculate_priority(deadline, importance, duration, difficulty, min_duration, 
                           max_duration, max_deadline, min_deadline, difficulty_preference):
        """
        Calculate a normalized weighted priority score for a task between 0 and 1.

        Args:
            deadline (float): Numeric representation of the task deadline.
            importance (int): Importance level (1 - 5).
            duration (int): Task duration in minutes.
            difficulty (int): Difficulty level (1 - 5).
            min_duration (int): Minimum duration among all tasks.
            max_duration (int): Maximum duration among all tasks.
            max_deadline (float): Latest deadline among all tasks.
            min_deadline (float): Earliest deadline among all tasks.
            difficulty_preference (str): "hardest" or "easiest".

        Returns:
            float: Priority score between 0 and 1.
        """

       
        if max_deadline == min_deadline:
            raise ValueError("Max and min deadlines cannot be the same.")
        
        normalized_deadline = 1 - (deadline - min_deadline)/ (max_deadline - min_deadline)

        normalized_importance = (importance - 1) / 4 

        if max_duration == min_duration:
            raise ValueError("Max and min durations cannot be the same.")
        normalized_duration = 1 - ( (duration - min_duration) / (max_duration - min_duration) )  # Inverse because shorter tasks are prioritized

        # the user chooses whether they want to prioritize the hardest or easiest tasks, which will affect the normalized difficulty score
        if difficulty_preference == "hardest":  
            normalized_difficulty = (difficulty - 1) / 4
        elif difficulty_preference == "easiest":  #
            normalized_difficulty = 1 - (difficulty - 1) / 4
        else:
            raise ValueError("Invalid difficulty preference. Choose 'hardest' or 'easiest'.")

        # Calculate the weighted priority score
        priority_score = (0.4 * normalized_deadline) + (0.35 * normalized_importance) + (0.15 * normalized_duration) + (0.1 * normalized_difficulty)
        return priority_score
 
    @staticmethod
    def sort_tasks_by_priority(tasks):
        if not tasks:
            return []
    
        return sorted(
        tasks, 
        key=lambda task: task.get('priority_score', 0), 
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

        task_dict = {task.id: task for task in sorted_tasks}
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
            visit(task.id)

        return ordered_tasks

     