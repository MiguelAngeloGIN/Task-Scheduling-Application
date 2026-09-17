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
led_team_id int null,
reset_token varchar(255),
reset_token_expires_at timestamp,
foreign key (company_id) references Company(company_id),
foreign key (led_team_id) references Team (team_id)
);




create table TeamMember (
team_id int not null,
user_id int not null,
primary key (team_id, user_id),
foreign key (team_id) references Team(team_id),
foreign key (user_id) references User(user_id)
);


create table Objective (
objective_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
progress decimal (5,2) default 0,
is_archived boolean default false, 
company_id int not null,
unique(name, company_id)
foreign key (company_id) references Company(company_id)
);



create table Task (
task_id int auto_increment primary key,
name varchar(50) not null,
description varchar(500),
status varchar(50) default 'pending',   -- pending, complete, overdue
importance int not null,
deadline timestamp not null,
team_id int not null,
objective_id int not null,
unique (name, objective_id),
foreign key (team_id) references Team(team_id),
foreign key (objective_id) references Objective (objective_id)
);






create table Dependency (
dependency_id int auto_increment primary key,
dependant int not null,
dependency int not null,
unique(dependant, dependency),
foreign key (dependant) references Task(task_id) on delete cascade,
foreign key (dependency) references Task(task_id) on delete cascade
);


create table Task_History(
task_history_id int auto_increment primary key,
action varchar(50) not null, -- create, complete, delete
description varchar(500), -- changes explanation
created_at timestamp default current_timestamp(),
author int not null,
task int not null,
foreign key (author) references User (user_id)
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

create index idx_user_company on user(company_id);


create index idx_task_team on Task(team_id);
create index idx_task_objective on Task(objective_id);

create index idx_dependency_dependant on Dependency(dependant);
create index idx_dependency_dependency on Dependency(dependency);

create index idx_history_task on Task_History(task);
create index idx_history_author on Task_History(author);

create index idx_team_member_user
on  TeamMember(user_id);

create index idx_user_led_team on user(led_team_id);


use Scheduler;


select * from invitation;
select * from user;
select * from teammember;
select * from team;
select * from objective;
select * from task;
select * from dependency;
select * from teammember;

describe task