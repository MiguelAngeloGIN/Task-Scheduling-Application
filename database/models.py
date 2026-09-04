import db_connection
from sqlalchemy import Integer, String, Numeric, Boolean, Column, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()


class Company(Base):
    __tablename__ = "Company"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    teams = relationship("Team", back_populates="company")
    users = relationship("User", back_populates="company")
    objectives = relationship("Objective", back_populates="company")

class Team(Base):
    __tablename__ = "Team"

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    company = relationship("Company", back_populates="teams")
    users = relationship("User", back_populates="team")
    tasks = relationship("Task", back_populates="team")

class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    team_id = Column(Integer, ForeignKey("Team.team_id"))
    company = relationship("Company", back_populates="users")
    team = relationship("Team", back_populates="users")
    task_histories = relationship("TaskHistory", back_populates="author_user")


class Objective(Base):
    __tablename__ = "Objective"

    objective_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    progress = Column(Numeric(5, 2), default=0)
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    company = relationship("Company", back_populates="objectives")
    tasks = relationship("Task", back_populates="objective")

class Task(Base):
    __tablename__ = "Task"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    status = Column(String(50), default="pending")  # pending, in progress, complete, overdue
    importance = Column(Integer)
    deadline = Column(TIMESTAMP)
    duration = Column(Integer)
    difficulty = Column(Integer)
    team_id = Column(Integer, ForeignKey("Team.team_id"))
    objective_id = Column(Integer, ForeignKey("Objective.objective_id"))
    team = relationship("Team", back_populates="tasks")
    objective = relationship("Objective", back_populates="tasks")
    task_histories = relationship("TaskHistory", back_populates="task_obj")
    dependant_dependencies = relationship("Dependency", foreign_keys="[Dependency.dependant]", back_populates="dependant_task")
    dependency_dependencies = relationship("Dependency", foreign_keys="[Dependency.dependency]", back_populates="dependency_task")

class Dependency(Base):
    __tablename__ = "Dependency"

    dependency_id = Column(Integer, primary_key=True, autoincrement=True)
    dependant = Column(Integer, ForeignKey("Task.task_id"))
    dependency = Column(Integer, ForeignKey("Task.task_id"))
    dependant_task = relationship("Task", foreign_keys=[dependant], back_populates="dependant_dependencies")
    dependency_task = relationship("Task", foreign_keys=[dependency], back_populates="dependency_dependencies")

class TaskHistory(Base):
    __tablename__ = "Task_History"

    task_history_id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(50), nullable=False)  # update, complete, delete, create
    description = Column(String(500))  # changes explanation
    old_value = Column(String(500))
    new_value = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    author = Column(Integer, ForeignKey("User.user_id"))
    task = Column(Integer, ForeignKey("Task.task_id"))
    author_user = relationship("User", foreign_keys=[author], back_populates="task_histories")
    task_obj = relationship("Task", foreign_keys=[task], back_populates="task_histories")