CREATE SCHEMA IF NOT EXISTS ex00 ;

SHOW search_path ;
SET search_path TO ex00 ;

create table ex00.Hospital (
    hospital_id serial primary key ,
    name varchar ,
    address varchar
) ;

create table ex00.Department (
    department_id serial primary key ,
    name varchar ,
    hospital_id int ,
    foreign key (hospital_id) references ex00.Hospital
    -- unique (name, hospital_id)
) ;

create table ex00.Doctor (
    id serial primary key ,
    name varchar ,
    department_id int ,
    foreign key (department_id) references ex00.Department
) ;

-- drop table ex00.Hospital cascade ;
-- drop table ex00.Department cascade ;
-- drop table ex00.Doctor cascade ;

insert into ex00.Hospital (name, address)
    values
        ('Sjukhusstock', 'Drottninggatan 3, Stockholm');

insert into ex00.Department (name, hospital_id) values
    ('Kardiologi', 1),
    ('Neurologi', 1);

insert into ex00.Doctor (name, department_id) values
    ('Dr. Abra Abrahamson', 1),
    ('Dr. Erika Eriksson', 1),
    ('Dr. Sven Svensson', 2);

select * from ex00.Hospital, ex00.Department, ex00.Doctor;

select h.name, d.name
from ex00.Hospital h
inner join ex00.Department d on h.hospital_id = d.hospital_id;