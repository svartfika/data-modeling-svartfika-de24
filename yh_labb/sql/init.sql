CREATE SCHEMA IF NOT EXISTS yh ;
SET search_path TO yh ;



CREATE TABLE IF NOT EXISTS yh.person (
    person_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    last_name VARCHAR,
    first_name VARCHAR,
    identity_number VARCHAR,
    address TEXT,
    phone VARCHAR,
    email_private VARCHAR
) ;



CREATE TABLE IF NOT EXISTS yh.affiliation_role (
    affiliation_role_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    description TEXT
) ;

CREATE TABLE IF NOT EXISTS yh.affiliation (
    affiliation_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_id INTEGER REFERENCES yh.person (person_id),
    affiliation_role_id INTEGER REFERENCES yh.affiliation_role (affiliation_role_id)
) ;



CREATE TABLE IF NOT EXISTS yh.employee_category (
    employee_category_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    description TEXT
) ;

CREATE TABLE IF NOT EXISTS yh.employee (
    employee_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id INTEGER REFERENCES yh.affiliation (affiliation_id),
    employee_category_id INTEGER REFERENCES yh.employee_category (employee_category_id),
    date_start DATE,
    date_end DATE
) ;


CREATE TABLE IF NOT EXISTS yh.consultant (
    consultant_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER REFERENCES yh.employee (employee_id),
    org_name VARCHAR,
    org_number VARCHAR,
    f_skatt BOOLEAN,
    rate_hourly MONEY,
    address TEXT
) ;

CREATE TABLE IF NOT EXISTS yh.full_time (
    full_time_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER REFERENCES yh.employee (employee_id),
    salary_montly MONEY,
    hours_weekly NUMERIC
) ;



CREATE TABLE IF NOT EXISTS yh.branch (
    branch_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    city VARCHAR,
    address VARCHAR
) ;

CREATE TABLE IF NOT EXISTS yh.program (
    program_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    code VARCHAR,
    cycle INTEGER,
    description TEXT,
    date_start DATE,
    date_end DATE    
) ;



CREATE TABLE IF NOT EXISTS yh.module_type (
    module_type_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    description TEXT   
) ;

CREATE TABLE IF NOT EXISTS yh.module (
    module_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_type_id INTEGER REFERENCES yh.module_type (module_type_id),
    branch_id INTEGER REFERENCES yh.branch (branch_id),
    name VARCHAR,
    code VARCHAR,
    description TEXT,
    date_start DATE,
    date_end DATE      
) ;

CREATE TABLE IF NOT EXISTS yh.course (
    course_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_id INTEGER REFERENCES yh.module (module_id),
    name VARCHAR,
    code VARCHAR,
    credits INTEGER,
    description TEXT,
    date_start DATE,
    date_end DATE   
) ;



CREATE TABLE IF NOT EXISTS yh.manager (
    manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER REFERENCES yh.employee (employee_id)
) ;

CREATE TABLE IF NOT EXISTS yh.teacher (
    teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER REFERENCES yh.employee (employee_id)
) ;

CREATE TABLE IF NOT EXISTS yh.student (
    student_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    affiliation_id INTEGER REFERENCES yh.affiliation (affiliation_id),
    program_id INTEGER REFERENCES yh.program (program_id),
    email_internal VARCHAR
) ;



CREATE TABLE IF NOT EXISTS yh.program_branch (
    program_branch_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id INTEGER REFERENCES yh.program (program_id),
    branch_id INTEGER REFERENCES yh.branch (branch_id)
) ;

CREATE TABLE IF NOT EXISTS yh.module_program (
    module_program_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    module_id INTEGER REFERENCES yh.module (module_id),
    program_id INTEGER REFERENCES yh.program (program_id)
) ;



CREATE TABLE IF NOT EXISTS yh.course_teacher (
    course_teacher_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER REFERENCES yh.course (course_id),
    teacher_id INTEGER REFERENCES yh.teacher (teacher_id)
) ;

CREATE TABLE IF NOT EXISTS yh.course_student (
    course_student_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    course_id INTEGER REFERENCES yh.course (course_id),
    student_id INTEGER REFERENCES yh.student (student_id)
) ;



CREATE TABLE IF NOT EXISTS yh.cohort (
    cohort_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR,
    code VARCHAR
) ;

CREATE TABLE IF NOT EXISTS yh.cohort_manager (
    cohort_manager_id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cohort_id INTEGER REFERENCES yh.cohort (cohort_id),
    manager_id INTEGER REFERENCES yh.manager (manager_id)
) ;

CREATE TABLE IF NOT EXISTS yh.student_cohort (
    student_cohort bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INTEGER REFERENCES yh.student (student_id),
    cohort_id INTEGER REFERENCES yh.cohort (cohort_id)
) ;