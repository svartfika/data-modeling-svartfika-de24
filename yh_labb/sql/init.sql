CREATE SCHEMA IF NOT EXISTS yh ;
SET search_path TO yh ;



-- MAIN ENTITIES

CREATE TABLE IF NOT EXISTS yh.person (
    person_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    last_name varchar(100) NOT NULL,
    first_name varchar(100) NOT NULL,
    identity_number varchar(100) NOT NULL,
    address text NOT NULL,
    phone varchar NOT NULL,
    email_private varchar NOT NULL,
    UNIQUE (identity_number)
) ;

CREATE TABLE IF NOT EXISTS yh.affiliation_role (
    affiliation_role_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    description text
) ;

CREATE TABLE IF NOT EXISTS yh.affiliation (
    affiliation_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_id bigint NOT NULL REFERENCES yh.person (person_id) ON DELETE CASCADE,
    affiliation_role_id bigint NOT NULL REFERENCES yh.affiliation_role (affiliation_role_id) ON DELETE RESTRICT,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (person_id, affiliation_role_id)
) ;



CREATE TABLE IF NOT EXISTS yh.employment_category (
    employment_category_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    description text
) ;

CREATE TABLE IF NOT EXISTS yh.employment (
    employment_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id bigint NOT NULL REFERENCES yh.affiliation (affiliation_id) ON DELETE CASCADE,
    employment_category_id bigint NOT NULL REFERENCES yh.employment_category (employment_category_id) ON DELETE RESTRICT,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (affiliation_id, employment_category_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.consultant (
    consultant_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id) ON DELETE CASCADE,
    org_name varchar(100),
    org_number varchar(100),
    f_skatt boolean,
    rate_hourly numeric(10,2),
    address text
) ;

CREATE TABLE IF NOT EXISTS yh.full_time (
    full_time_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id) ON DELETE CASCADE,
    salary_monthly numeric(10,2),
    hours_weekly smallint
) ;



CREATE TABLE IF NOT EXISTS yh.manager (
    manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id) ON DELETE CASCADE,
    UNIQUE (employment_id)
) ;

CREATE TABLE IF NOT EXISTS yh.teacher (
    teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id) ON DELETE CASCADE,
    UNIQUE (employment_id)
) ;



CREATE TABLE IF NOT EXISTS yh.branch (
    branch_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL,
    city varchar(100) NOT NULL,
    address varchar(100),
    description text,
    UNIQUE (name, city)
) ;

CREATE TABLE IF NOT EXISTS yh.program (
    program_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    cycle smallint NOT NULL CHECK (cycle BETWEEN 1 AND 3),
    description text,
    UNIQUE (code, cycle)
) ;

CREATE TABLE IF NOT EXISTS yh.course (
    course_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id bigint NOT NULL REFERENCES yh.program (program_id) ON DELETE RESTRICT,
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    credits smallint NOT NULL,
    description text,
    UNIQUE (program_id, code)
) ;



CREATE TABLE IF NOT EXISTS yh.module_type (
    module_type_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    description text
) ;

CREATE TABLE IF NOT EXISTS yh.module (
    module_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_type_id bigint NOT NULL REFERENCES yh.module_type (module_type_id) ON DELETE RESTRICT,
    branch_id bigint NOT NULL REFERENCES yh.branch (branch_id) ON DELETE RESTRICT,
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    description text,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (branch_id, code, date_start) 
) ;



CREATE TABLE IF NOT EXISTS yh.cohort (
    cohort_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id bigint NOT NULL REFERENCES yh.program (program_id) ON DELETE RESTRICT,
    branch_id bigint NOT NULL REFERENCES yh.branch (branch_id) ON DELETE RESTRICT,
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (program_id, code, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.student (
    student_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id bigint NOT NULL REFERENCES yh.affiliation (affiliation_id) ON DELETE CASCADE,
    email_internal varchar(100) NOT NULL,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (affiliation_id, email_internal)
) ;



-- JUNCTION TABLES

CREATE TABLE IF NOT EXISTS yh.program_branch (
    program_branch_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id bigint NOT NULL REFERENCES yh.program (program_id) ON DELETE CASCADE,
    branch_id bigint NOT NULL REFERENCES yh.branch (branch_id) ON DELETE RESTRICT,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (program_id, branch_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.module_program (
    module_program_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_id bigint NOT NULL REFERENCES yh.module (module_id) ON DELETE CASCADE,
    program_id bigint NOT NULL REFERENCES yh.program (program_id) ON DELETE RESTRICT,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (module_id, program_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.course_module (
    course_module_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id bigint NOT NULL REFERENCES yh.course (course_id) ON DELETE CASCADE,
    module_id bigint NOT NULL REFERENCES yh.module (module_id) ON DELETE CASCADE,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (course_id, module_id, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.teacher_course (
    course_teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    teacher_id bigint NOT NULL REFERENCES yh.teacher (teacher_id) ON DELETE CASCADE,
    course_module_id bigint NOT NULL REFERENCES yh.course_module (course_module_id) ON DELETE CASCADE,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (teacher_id, course_module_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.student_course (
    student_course_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES yh.student (student_id) ON DELETE CASCADE,
    course_module_id bigint NOT NULL REFERENCES yh.course_module (course_module_id) ON DELETE CASCADE,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (student_id, course_module_id, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.cohort_manager (
    cohort_manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cohort_id bigint NOT NULL REFERENCES yh.cohort (cohort_id) ON DELETE CASCADE,
    manager_id bigint NOT NULL REFERENCES yh.manager (manager_id) ON DELETE CASCADE,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (cohort_id, manager_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.student_cohort (
    student_cohort_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES yh.student (student_id) ON DELETE CASCADE,
    cohort_id bigint NOT NULL REFERENCES yh.cohort (cohort_id) ON DELETE CASCADE,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (student_id, cohort_id, date_start)
) ;



-- DEFAULT VALUES

INSERT INTO yh.affiliation_role (name) 
VALUES ('EMPLOYEE'), ('MANAGER'), ('STUDENT'), ('TEACHER')
ON CONFLICT (name) DO NOTHING ;

INSERT INTO yh.employment_category (name) 
VALUES ('CONSULTANT'), ('FULL_TIME')
ON CONFLICT (name) DO NOTHING;

INSERT INTO yh.module_type (name) 
VALUES ('EXTRA'), ('SEMESTER'), ('WORKSHOP')
ON CONFLICT (name) DO NOTHING;
