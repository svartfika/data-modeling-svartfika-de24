from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class Person(BaseModel):
    person_id: Optional[int]
    last_name: str
    first_name: str
    identity_number: str
    address: str
    phone: str
    email_private: EmailStr


class AffiliationRole(BaseModel):
    affiliation_role_id: Optional[int]
    name: str
    description: Optional[str] = None


class Affiliation(BaseModel):
    affiliation_id: Optional[int]
    person_id: int
    affiliation_role_id: int


class EmploymentCategory(BaseModel):
    employment_category_id: Optional[int]
    name: str
    description: Optional[str] = None


class Employment(BaseModel):
    employment_id: Optional[int]
    affiliation_id: int
    employment_category_id: int
    date_start: date
    date_end: Optional[date] = None


class Consultant(BaseModel):
    consultant_id: Optional[int]
    employment_id: int
    org_name: Optional[str] = None
    org_number: Optional[str] = None
    f_skatt: Optional[bool] = None
    rate_hourly: Optional[float] = None
    address: Optional[str] = None


class FullTime(BaseModel):
    full_time_id: Optional[int]
    employment_id: int
    salary_monthly: Optional[float] = None
    hours_weekly: Optional[int] = None


class Branch(BaseModel):
    branch_id: Optional[int]
    name: str
    city: str
    address: Optional[str] = None
    description: Optional[str] = None


class Program(BaseModel):
    program_id: Optional[int]
    name: str
    code: str
    cycle: int
    description: Optional[str] = None
    date_start: date
    date_end: Optional[date] = None


class ModuleType(BaseModel):
    module_type_id: Optional[int]
    name: str
    description: Optional[str] = None


class Module(BaseModel):
    module_id: Optional[int]
    module_type_id: int
    branch_id: int
    name: str
    code: str
    description: Optional[str] = None
    date_start: date
    date_end: Optional[date] = None


class Course(BaseModel):
    course_id: Optional[int]
    module_id: int
    name: str
    code: str
    credits: int
    description: Optional[str] = None
    date_start: date
    date_end: Optional[date] = None


class Manager(BaseModel):
    manager_id: Optional[int]
    employment_id: int


class Teacher(BaseModel):
    teacher_id: Optional[int]
    employment_id: int


class Student(BaseModel):
    student_id: Optional[int]
    affiliation_id: int
    program_id: int
    email_internal: str
    date_start: date
    date_end: Optional[date] = None


class Cohort(BaseModel):
    cohort_id: Optional[int]
    program_id: int
    name: str
    code: str
    date_start: date
    date_end: Optional[date] = None


class ProgramBranch(BaseModel):
    program_branch_id: Optional[int]
    program_id: int
    branch_id: int


class ModuleProgram(BaseModel):
    module_program_id: Optional[int]
    module_id: int
    program_id: int


class CourseTeacher(BaseModel):
    course_teacher_id: Optional[int]
    course_id: int
    teacher_id: int


class CourseStudent(BaseModel):
    course_student_id: Optional[int]
    course_id: int
    student_id: int


class CohortManager(BaseModel):
    cohort_manager_id: Optional[int]
    cohort_id: int
    manager_id: int


class StudentCohort(BaseModel):
    student_cohort_id: Optional[int]
    student_id: int
    cohort_id: int
