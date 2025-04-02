CREATE SCHEMA IF NOT EXISTS yh ;
SET search_path TO yh ;



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
    person_id bigint NOT NULL REFERENCES yh.person (person_id),
    affiliation_role_id bigint NOT NULL REFERENCES yh.affiliation_role (affiliation_role_id),
    UNIQUE (person_id, affiliation_role_id)
) ;



CREATE TABLE IF NOT EXISTS yh.employment_category (
    employment_category_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    description text
) ;

CREATE TABLE IF NOT EXISTS yh.employment (
    employment_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id bigint NOT NULL REFERENCES yh.affiliation (affiliation_id),
    employment_category_id bigint NOT NULL REFERENCES yh.employment_category (employment_category_id),
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (affiliation_id, employment_category_id, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.consultant (
    consultant_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id),
    org_name varchar(100),
    org_number varchar(100),
    f_skatt boolean,
    rate_hourly numeric(10,2),
    address text
) ;

CREATE TABLE IF NOT EXISTS yh.full_time (
    full_time_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id),
    salary_monthly numeric(10,2),
    hours_weekly smallint
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
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (code, cycle, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.module_type (
    module_type_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name varchar(100) NOT NULL UNIQUE,
    description text
) ;

CREATE TABLE IF NOT EXISTS yh.module (
    module_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_type_id bigint NOT NULL REFERENCES yh.module_type (module_type_id),
    branch_id bigint NOT NULL REFERENCES yh.branch (branch_id),
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    description text,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (branch_id, code, date_start) 
) ;

CREATE TABLE IF NOT EXISTS yh.course (
    course_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_id bigint NOT NULL REFERENCES yh.module (module_id),
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    credits smallint NOT NULL,
    description text,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (module_id, code, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.manager (
    manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id),
    UNIQUE (employment_id)
) ;

CREATE TABLE IF NOT EXISTS yh.teacher (
    teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employment_id bigint NOT NULL REFERENCES yh.employment (employment_id),
    UNIQUE (employment_id)
) ;



CREATE TABLE IF NOT EXISTS yh.student (
    student_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id bigint NOT NULL REFERENCES yh.affiliation (affiliation_id),
    program_id bigint NOT NULL REFERENCES yh.program (program_id),
    email_internal varchar(100) NOT NULL,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (affiliation_id, program_id, date_start)
) ;

CREATE TABLE IF NOT EXISTS yh.cohort (
    cohort_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id bigint NOT NULL REFERENCES yh.program (program_id),
    name varchar(100) NOT NULL,
    code varchar(100) NOT NULL,
    date_start date NOT NULL,
    date_end date CHECK (date_end IS NULL OR date_end > date_start),
    UNIQUE (program_id, code, date_start)
) ;



CREATE TABLE IF NOT EXISTS yh.program_branch (
    program_branch_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id bigint NOT NULL REFERENCES yh.program (program_id),
    branch_id bigint NOT NULL REFERENCES yh.branch (branch_id),
    UNIQUE (program_id, branch_id)
) ;

CREATE TABLE IF NOT EXISTS yh.module_program (
    module_program_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_id bigint NOT NULL REFERENCES yh.module (module_id),
    program_id bigint NOT NULL REFERENCES yh.program (program_id),
    UNIQUE (module_id, program_id)
) ;



CREATE TABLE IF NOT EXISTS yh.course_teacher (
    course_teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id bigint NOT NULL REFERENCES yh.course (course_id),
    teacher_id bigint NOT NULL REFERENCES yh.teacher (teacher_id),
    UNIQUE (course_id, teacher_id)
) ;

CREATE TABLE IF NOT EXISTS yh.course_student (
    course_student_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id bigint NOT NULL REFERENCES yh.course (course_id),
    student_id bigint NOT NULL REFERENCES yh.student (student_id),
    UNIQUE (course_id, student_id)
) ;



CREATE TABLE IF NOT EXISTS yh.cohort_manager (
    cohort_manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cohort_id bigint NOT NULL REFERENCES yh.cohort (cohort_id),
    manager_id bigint NOT NULL REFERENCES yh.manager (manager_id),
    UNIQUE (cohort_id, manager_id)
) ;

CREATE TABLE IF NOT EXISTS yh.student_cohort (
    student_cohort_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id bigint NOT NULL REFERENCES yh.student (student_id),
    cohort_id bigint NOT NULL REFERENCES yh.cohort (cohort_id),
    UNIQUE (student_id, cohort_id)
) ;