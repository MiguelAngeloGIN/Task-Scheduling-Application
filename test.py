from crud.add_crud import Add_Sql

add_company = Add_Sql.add_company
add_team = Add_Sql.add_team
add_user = Add_Sql.add_user
add_objective = Add_Sql.add_objective
add_task = Add_Sql.add_task
add_dependency = Add_Sql.add_dependency
add_task_history = Add_Sql.add_task_history

# 1. Company

add_company("Tech Solutions")

# 2. Team
add_team("Development", 1)

# 3. User
add_user(
    "Miguel",
    "Silva",
    "miguel@test.com",
    "hashed_password",
    1,      # company_id
    1,      # team_id
    True    # is_admin
)

# 4. Objective
add_objective(
    "Complete Scheduler",
    "Develop the Scheduler application",
    1       # company_id
)

# 5. Task 1
add_task(
    "Create database",
    "Create the Scheduler database",
    "pending",
    5,
    "2026-09-30 18:00:00",
    120,
    3,
    1,      # team_id
    1       # objective_id
)

# 6. Task 2
add_task(
    "Implement CRUD",
    "Implement CRUD operations",
    "pending",
    4,
    "2026-10-05 18:00:00",
    180,
    4,
    1,
    1
)

# 7. Dependency
# Task 2 depends on Task 1
add_dependency(
    2,      # dependant_id
    1       # dependency_id
)

# 8. Task History
add_task_history(
    "create",
    "Task was created",
    None,
    "Create database",
    1,      # author_id
    1       # task_id
)