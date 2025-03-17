-- setup


CREATE SCHEMA IF NOT EXISTS ex10 ;

SHOW search_path ;
SET search_path TO ex10 ;  -- set schema for current session


-- entities


CREATE TABLE hospital (
    hospital_id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(50)
) ;

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(50)
) ;

CREATE TABLE doctor (
    doctor_id SERIAL PRIMARY KEY,
    doctor_name VARCHAR(50),
    identity_number VARCHAR UNIQUE
) ;


-- composites


CREATE TABLE hospital_department (
    hospital_id INTEGER references hospital,
    department_id INTEGER references department,
    PRIMARY KEY (hospital_id, department_id)
) ;

CREATE TABLE hospital_doctor (
    hospital_id INTEGER references hospital,
    doctor_id INTEGER references doctor,
    PRIMARY KEY (hospital_id, doctor_id)
) ;

CREATE TABLE department_doctor (
    department_id INTEGER references department,
    doctor_id INTEGER references doctor,
    PRIMARY KEY (department_id, doctor_id)
) ;


-- ingest initial data


INSERT INTO hospital (hospital_name)
VALUES
    ('Danderyds sjukhus'),
    ('Södersjukhuset'),
    ('S:t Görans sjukhus') ;

INSERT INTO department (department_name)
VALUES
    ('Diabetesmottagning'),
    ('Förlossning'),
    ('Hjärtcentrum'),
    ('Kirurgmottagningen'),
    ('Neurologiska mottagningen') ;

INSERT INTO doctor (doctor_name, identity_number)
VALUES
    ('Alice Aliceson', '123-456'),
    ('Bob Bobson', '789-012'),
    ('Carl Carlson', '345-678'),
    ('Dave Daveson', '890-123') ;


-- link data


INSERT INTO hospital_department (hospital_id, department_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 4),
    (3, 2),
    (3, 5) ;

INSERT INTO hospital_doctor (hospital_id, doctor_id)
VALUES
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 3),
    (3, 4),
    (3, 2) ;

INSERT INTO department_doctor (department_id, doctor_id)
VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 4),
    (3, 3),
    (4, 2) ;

-- drop

-- drop table ex10.hospital cascade ;
-- drop table ex10.department cascade ;
-- drop table ex10.doctor cascade ;