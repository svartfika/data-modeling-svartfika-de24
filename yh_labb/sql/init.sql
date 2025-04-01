CREATE SCHEMA IF NOT EXISTS yh ;
SET search_path TO yh ;



CREATE TABLE IF NOT EXISTS yh.person (
   person_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.affiliation (
   affiliation_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.affiliation_role (
   affiliation_role_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.employee (
    employee_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.student (
    student_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.branch (
    branch_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.program (
    program_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.module_type (
    module_type_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.module (
    module_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.course (
    course_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.employee_category (
   employee_category_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.consultant (
    consultant_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.full_time (
    full_time_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.teacher (
    teacher_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.manager (
    manager_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.program_branch (
    program_branch_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.module_program (
    module_program_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.course_teacher (
    course_teacher_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.course_student (
    course_student_id SERIAL PRIMARY KEY
) ;



CREATE TABLE IF NOT EXISTS yh.cohort (
    cohort_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.cohort_manager (
    cohort_manager_id SERIAL PRIMARY KEY
) ;

CREATE TABLE IF NOT EXISTS yh.student_cohort (
    student_cohort SERIAL PRIMARY KEY
) ;