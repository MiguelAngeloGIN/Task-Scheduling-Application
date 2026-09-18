from sqlalchemy import (
    TIMESTAMP,
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from database import db_connection

Base = declarative_base()

Session = sessionmaker(bind=db_connection.engine)
session = Session()


class Company(Base):
    __tablename__ = "Company"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    teams = relationship("Team", back_populates="company")
    users = relationship("User", back_populates="company")
    objectives = relationship("Objective", back_populates="company")
    invitations = relationship("Invitation", back_populates="company")

class Team(Base):
    __tablename__ = "Team"

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    is_active = Column(Boolean, default=True)
    company = relationship("Company", back_populates="teams")
    team_members = relationship("TeamMember", back_populates="team")
    leaders = relationship("User", foreign_keys="User.led_team_id", back_populates="led_team")
    tasks = relationship("Task", back_populates="team")


class User(Base):
    __tablename__ = "User"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    reset_token = Column(String(255))
    reset_token_expires_at = Column(TIMESTAMP)
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    led_team_id = Column (Integer, ForeignKey("Team.team_id"))
    company = relationship("Company", back_populates="users")
    task_histories = relationship("TaskHistory", back_populates="author_user")
    sent_invitations = relationship("Invitation", back_populates="inviter")
    team_memberships = relationship("TeamMember", back_populates="user")
    led_team = relationship("Team",   foreign_keys=[led_team_id], back_populates="leaders"
)

class TeamMember(Base):
    __tablename__ = "TeamMember"

    team_id = Column(Integer, ForeignKey("Team.team_id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("User.user_id"), primary_key=True)
    team = relationship("Team", back_populates="team_members")
    user = relationship("User", back_populates="team_memberships")
    

class Objective(Base):
    __tablename__ = "Objective"

    objective_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(500))
    progress = Column(Numeric(5, 2), default=0)
    is_archived = Column(Boolean, default=False)
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
    team_id = Column(Integer, ForeignKey("Team.team_id"))
    objective_id = Column(Integer, ForeignKey("Objective.objective_id"))
    team = relationship("Team", back_populates="tasks")
    objective = relationship("Objective", back_populates="tasks")
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
    action = Column(String(50), nullable=False)  # create, complete, delete
    description = Column(String(500))  # explanation
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    author = Column(Integer, ForeignKey("User.user_id"))
    task = Column(Integer)
    author_user = relationship("User", foreign_keys=[author], back_populates="task_histories")
    


class Invitation(Base):
    __tablename__ = "Invitation"

    invitation_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("Company.company_id"), nullable=False)
    invited_by = Column(Integer, ForeignKey("User.user_id"), nullable=False)
    invited_email = Column(String(50), nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    expires_at = Column(TIMESTAMP)
    company = relationship("Company", foreign_keys=[company_id], back_populates="invitations")
    inviter = relationship("User", foreign_keys=[invited_by], back_populates="sent_invitations")
    
