create schema Scheduler;

use Scheduler;

create table Company (
company_id int auto_increment primary key,
name varchar (50) not null,
is_active boolean default true,
created_at timestamp  default current_timestamp()
);

create table Team (
team_id int auto_increment primary key,
name varchar (50) not null,
created_at timestamp default current_timestamp(),
company_id int,
foreign key (company_id) references Company(company_id)
);

create table User (
user_id int auto_increment primary key,
first_name varchar(50) not null,
last_name varchar(50) not null,
email varchar(50) not null,
password_hash varchar (255) not null,
is_admin boolean default false,
created_at timestamp default current_timestamp(),
company_id int,
team_id int,
reset_token varchar(255),
reset_token_expires_at timestamp,
foreign key (company_id) references Company(company_id),
foreign key (team_id) references Team(team_id)
);



create table Objective (
objective_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
progress decimal (5,2) default 0,
company_id int,
foreign key (company_id) references Company(company_id)
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
team_id int,
objective_id int,
foreign key (team_id) references Team(team_id),
foreign key (objective_id) references Objective (objective_id)
);


create table Dependency (
dependency_id int auto_increment primary key,
dependant int,
dependency int,
foreign key (dependant) references Task(task_id),
foreign key (dependency) references Task(task_id)
);


create table Task_History(
task_history_id int auto_increment primary key,
action varchar(50) not null, -- update, complete, delete, create
description varchar(500), -- changes explanation
old_value varchar(500),
new_value varchar(500),
created_at timestamp default current_timestamp(),
author int,
task int,
foreign key (author) references User (user_id),
foreign key (task) references Task (task_id)
);






