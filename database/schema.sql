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
company_id int not null,
unique (company_id, name),
foreign key (company_id) references Company(company_id) on delete cascade
);

create table User (
user_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
email varchar(50) not null unique,
password_hash varchar (255) not null,
is_admin boolean default false,
created_at timestamp default current_timestamp(),
company_id int not null,
team_id int not null,
reset_token varchar(255),
reset_token_expires_at timestamp,
foreign key (company_id) references Company(company_id) on delete cascade,
foreign key (team_id) references Team(team_id) on delete cascade
);



create table Objective (
objective_id int auto_increment primary key,
name varchar(50) not null unique,
description varchar(500),
progress decimal (5,2) default 0,
company_id int not null,
foreign key (company_id) references Company(company_id) on delete cascade
);



create table Task (
task_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
status varchar(50) default 'pending',   -- pending, in progress, complete, overdue
importance int,
deadline timestamp,
duration int,
difficulty int,
team_id int not null,
objective_id int not null,
foreign key (team_id) references Team(team_id) on delete cascade,
foreign key (objective_id) references Objective (objective_id) on delete cascade
);


create table Dependency (
dependency_id int auto_increment primary key,
dependant int not null,
dependency int not null,
foreign key (dependant) references Task(task_id) on delete cascade,
foreign key (dependency) references Task(task_id) on delete cascade
);


create table Task_History(
task_history_id int auto_increment primary key,
action varchar(50) not null, -- update, complete, delete, create
description varchar(500), -- changes explanation
old_value varchar(500),
new_value varchar(500),
created_at timestamp default current_timestamp(),
author int not null,
task int not null,
foreign key (author) references User (user_id) on delete cascade,
foreign key (task) references Task (task_id) on delete cascade
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



ALTER TABLE User ADD UNIQUE (email);
ALTER TABLE Company ADD UNIQUE (name);
ALTER TABLE Team ADD UNIQUE (company_id, name);


CREATE INDEX idx_user_company ON User(company_id);
CREATE INDEX idx_user_team ON User(team_id);

CREATE INDEX idx_task_team ON Task(team_id);
CREATE INDEX idx_task_objective ON Task(objective_id);

CREATE INDEX idx_dependency_dependant ON Dependency(dependant);
CREATE INDEX idx_dependency_dependency ON Dependency(dependency);

CREATE INDEX idx_history_task ON Task_History(task);
CREATE INDEX idx_history_author ON Task_History(author);






