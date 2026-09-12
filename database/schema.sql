create schema Scheduler;

use Scheduler;

create table Company (
company_id int auto_increment primary key,
name varchar (50) not null unique,
is_active boolean default true,
created_at timestamp  default current_timestamp()
);

create table Team (
team_id int auto_increment primary key,
name varchar (50) not null,
created_at timestamp default current_timestamp(),
is_active boolean default true, 
company_id int not null,
leader_id int,   -- fk from user added later
unique (company_id, name),
foreign key (company_id) references Company(company_id)
);

create table User (
user_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
email varchar(50) not null unique,
password_hash varchar (255) not null,
is_admin boolean default false,
created_at timestamp default current_timestamp(),
company_id int null,
team_id int null,
reset_token varchar(255),
reset_token_expires_at timestamp,
foreign key (company_id) references Company(company_id),
foreign key (team_id) references Team(team_id)
);

ALTER TABLE Team
ADD CONSTRAINT fk_team_leader
FOREIGN KEY (leader_id) REFERENCES User(user_id);



create table Objective (
objective_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
progress decimal (5,2) default 0,
is_archived boolean default false, 
company_id int not null,
foreign key (company_id) references Company(company_id)
);

create table Task (
task_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
status varchar(50) default 'pending',   -- pending, complete, overdue
importance int,
deadline timestamp,
duration int,
difficulty int,
team_id int not null,
objective_id int not null,
foreign key (team_id) references Team(team_id),
foreign key (objective_id) references Objective (objective_id)
);


create table Dependency (
dependency_id int auto_increment primary key,
dependant int not null,
dependency int not null,
unique(dependant, dependency),
foreign key (dependant) references Task(task_id),
foreign key (dependency) references Task(task_id)
);


create table Task_History(
task_history_id int auto_increment primary key,
action varchar(50) not null, -- update, complete, delete, create
description varchar(500), -- changes explanation
old_value JSON,
new_value JSON,
created_at timestamp default current_timestamp(),
author int not null,
task int not null,
foreign key (author) references User (user_id),
foreign key (task) references Task (task_id) 
);

create table Invitation (
 invitation_id int auto_increment primary key,
 company_id int not null,
 invited_email varchar (50) not null,
 invited_by int not null,
 token varchar(255) not null unique,
 created_at timestamp  default current_timestamp,
 expires_at timestamp,
 foreign key (company_id) references Company(company_id),
 foreign key (invited_by) references User(user_id)
);

CREATE INDEX idx_user_company ON User(company_id);
CREATE INDEX idx_user_team ON User(team_id);

CREATE INDEX idx_task_team ON Task(team_id);
CREATE INDEX idx_task_objective ON Task(objective_id);

CREATE INDEX idx_dependency_dependant ON Dependency(dependant);
CREATE INDEX idx_dependency_dependency ON Dependency(dependency);

CREATE INDEX idx_history_task ON Task_History(task);
CREATE INDEX idx_history_author ON Task_History(author);










