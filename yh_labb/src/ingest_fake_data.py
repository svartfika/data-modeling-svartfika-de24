from datetime import date, datetime, timedelta
from itertools import batched
from typing import Literal
import random

from mimesis.providers.address import Address as AddressProvider
from mimesis.providers.finance import Finance as FinanceProvider
from mimesis.providers.person import Person as PersonProvider
from mimesis.random import Random as MimesisRandom


from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL, create_engine, select
from sqlalchemy.ext.automap import automap_base, AutomapBase
from sqlalchemy.orm import Session


class PostgresSettings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default="5432")
    user: str = Field(default="postgres")
    password: SecretStr = Field(default_factory=lambda: SecretStr(""))
    dbname: str = Field(default="postgres_db")


class Database(BaseSettings):
    dbschema: str = Field(default="yh")


class Settings(BaseSettings):
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    database: Database = Field(default_factory=Database)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="_",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


postgres_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.postgres.user,
    password=settings.postgres.password.get_secret_value(),
    host=settings.postgres.host,
    port=settings.postgres.port,
    database=settings.postgres.dbname,
)

engine = create_engine(postgres_url)


Base: AutomapBase = automap_base()
Base.prepare(autoload_with=engine, schema=settings.database.dbschema)


Person = Base.classes.person

AffiliationRole = Base.classes.affiliation_role
Affiliation = Base.classes.affiliation

EmploymentCategory = Base.classes.employment_category
Employment = Base.classes.employment
Consultant = Base.classes.consultant
FullTime = Base.classes.full_time

Branch = Base.classes.branch
Program = Base.classes.program

ModuleType = Base.classes.module_type
Module = Base.classes.module
Course = Base.classes.course

Manager = Base.classes.manager
Teacher = Base.classes.teacher
Student = Base.classes.student
Cohort = Base.classes.cohort

ProgramBranch = Base.classes.program_branch
ModuleProgram = Base.classes.module_program
CourseTeacher = Base.classes.course_teacher
CourseStudent = Base.classes.course_student
CohortManager = Base.classes.cohort_manager
StudentCohort = Base.classes.student_cohort


def get_random_date() -> datetime.date:
    return date(datetime.now().year, 1, 1) + timedelta(days=random.randint(0, 364))


def get_random_date_interval(date_start: date, date_end: date) -> datetime.date:
    return date_start + timedelta(days=random.randint(0, (date_end - date_start).days))


def add_person(s: Session) -> int:
    fake_person = PersonProvider()
    fake_address = AddressProvider()

    person = Person(
        last_name=fake_person.last_name(),
        first_name=fake_person.first_name(),
        identity_number=fake_person.identifier("########-####"),
        address=fake_address.address(),
        phone=fake_person.phone_number(),
        email_private=fake_person.email(),
    )

    s.add(person)
    s.flush()

    return person.person_id


def add_affiliation(
    s: Session,
    person_id: int,
    affiliation_role_name: Literal["EMPLOYEE", "MANAGER", "STUDENT", "TEACHER"],
) -> int:
    role_id = s.scalar(
        select(
            AffiliationRole.affiliation_role_id,
        ).where(
            AffiliationRole.name == affiliation_role_name,
        )
    )

    affiliation = Affiliation(person_id=person_id, affiliation_role_id=role_id)

    s.add(affiliation)
    s.flush()

    return affiliation.affiliation_id


def add_employment(
    s: Session,
    affiliation_id: int,
    employment_category_name: Literal["CONSULTANT", "FULL_TIME"],
    date_start: date,
    date_end: date | None = None,
) -> int:
    category_id = s.scalar(
        select(
            EmploymentCategory.employment_category_id,
        ).where(
            EmploymentCategory.name == employment_category_name,
        )
    )

    employment = Employment(
        affiliation_id=affiliation_id,
        employment_category_id=category_id,
        date_start=date_start,
    )

    if date_end:
        employment.date_end = date_end

    s.add(employment)
    s.flush()

    return employment.employment_id


def add_consultant(s: Session, employment_id: int) -> int:
    fake_finance = FinanceProvider()
    fake_random = MimesisRandom()
    fake_address = AddressProvider()

    consultant = Consultant(
        employment_id=employment_id,
        org_name=fake_finance.company(),
        org_number=fake_random.generate_string_by_mask("####-####"),
        f_skatt=next(iter(fake_random.choices([True, False]))),
        rate_hourly=fake_finance.price(500, 1500),
        address=fake_address.address(),
    )

    s.add(consultant)
    s.flush()

    return consultant.consultant_id


def add_full_time(s: Session, employment_id: int) -> int:
    fake_finance = FinanceProvider()
    fake_random = MimesisRandom()

    full_time = FullTime(
        employment_id=employment_id,
        salary_monthly=fake_finance.price(8000, 40000),
        hours_weekly=fake_random.randint(16, 40),
    )

    s.add(full_time)
    s.flush()

    return full_time.full_time_id


def add_manager(s: Session, employment_id: int) -> int:
    manager = Manager(employment_id=employment_id)

    s.add(manager)
    s.flush()

    return manager.manager_id


def add_teacher(s: Session, employment_id: int) -> int:
    teacher = Teacher(employment_id=employment_id)

    s.add(teacher)
    s.flush()

    return teacher.teacher_id


def add_employee(
    s: Session,
    person_id: int,
    affiliation_role_name: Literal["EMPLOYEE", "MANAGER", "TEACHER"],
    employment_category_name: Literal["CONSULTANT", "FULL_TIME"],
    date_start: date,
    date_end: date | None = None,
) -> int:
    affiliation_id = add_affiliation(
        s,
        person_id,
        affiliation_role_name=affiliation_role_name,
    )
    employment_id = add_employment(
        s,
        affiliation_id,
        employment_category_name=employment_category_name,
        date_start=date_start,
        date_end=date_end,
    )

    if employment_category_name == "CONSULTANT":
        add_consultant(s, employment_id)
    elif employment_category_name == "FULL_TIME":
        add_full_time(s, employment_id)
    else:
        raise KeyError(f"employment_category_name '{employment_category_name}' not found")

    if affiliation_role_name == "MANAGER":
        return add_manager(s, employment_id)
    elif affiliation_role_name == "TEACHER":
        return add_teacher(s, employment_id)
    else:
        raise KeyError(f"affiliation_role_name '{affiliation_role_name}' not found")


def add_branch(s: Session, *, name: str | None = None, city: str | None = None) -> int:
    fake_finance = FinanceProvider()
    fake_address = AddressProvider()

    branch = Branch(
        name=name or fake_finance.company(),
        city=city or fake_address.city(),
        address=fake_address.address(),
    )

    s.add(branch)
    s.flush()

    return branch.branch_id


def add_program(
    s: Session,
    date_start: date,
    date_end: date | None = None,
    *,
    name: str | None = None,
) -> int:
    fake_finance = FinanceProvider()
    fake_random = MimesisRandom()

    program = Program(
        name=name or fake_finance.company(),
        code=fake_random.generate_string_by_mask("@@##"),
        cycle=fake_random.randint(1, 3),
        date_start=date_start,
    )

    if date_end:
        program.date_end = date_end

    s.add(program)
    s.flush()

    return program.program_id


def add_program_branch(s: Session, program_id: int, branch_id: int) -> int:
    program_branch = ProgramBranch(
        program_id=program_id,
        branch_id=branch_id,
    )

    s.add(program_branch)
    s.flush()

    return program_branch.program_branch_id


def add_module_program(s: Session, module_id: int, program_id: int) -> int:
    module_program = ModuleProgram(
        module_id=module_id,
        program_id=program_id,
    )

    s.add(module_program)
    s.flush()

    return module_program.module_program_id


def add_module(
    s: Session,
    module_type_name: Literal["EXTRA", "PROGRAM", "WORKSHOP"],
    branch_id: int,
    date_start: date,
    date_end: date | None = None,
) -> int:
    type_id = s.scalar(
        select(
            ModuleType.module_type_id,
        ).where(
            ModuleType.name == module_type_name,
        )
    )

    fake_random = MimesisRandom()

    module = Module(
        module_type_id=type_id,
        branch_id=branch_id,
        name=fake_random.generate_string_by_mask("@@@@@@##"),
        code=fake_random.generate_string_by_mask("@@##"),
        date_start=date_start,
    )

    if date_end:
        module.date_end = date_end

    s.add(module)
    s.flush()

    return module.module_id


def add_course(
    s: Session,
    module_id: int,
    date_start: date,
    date_end: date | None = None,
    *,
    name: str | None,
) -> int:
    fake_random = MimesisRandom()

    course = Course(
        module_id=module_id,
        name=name or fake_random.generate_string_by_mask("@@@@@@##"),
        code=fake_random.generate_string_by_mask("@@##"),
        credits=fake_random.randint(10, 40),
        date_start=date_start,
    )

    if date_end:
        course.date_end = date_end

    s.add(course)
    s.flush()

    return course.course_id


def add_course_teacher(s: Session, course_id: int, teacher_id: int) -> int:
    course_teacher = CourseTeacher(
        course_id=course_id,
        teacher_id=teacher_id,
    )

    s.add(course_teacher)
    s.flush()

    return course_teacher.course_teacher_id


def add_course_student(s: Session, course_id: int, student_id: int) -> int:
    course_student = CourseStudent(
        course_id=course_id,
        student_id=student_id,
    )

    s.add(course_student)
    s.flush()

    return course_student.course_student_id


def add_cohort(
    s: Session,
    program_id: int,
    branch_id: int,
    date_start: date,
    date_end: date | None = None,
) -> int:
    fake_random = MimesisRandom()

    cohort = Cohort(
        program_id=program_id,
        branch_id=branch_id,
        name=fake_random.generate_string_by_mask("@@@@@@##"),
        code=fake_random.generate_string_by_mask("@@##"),
        date_start=date_start,
    )

    if date_end:
        cohort.date_end = date_end

    s.add(cohort)
    s.flush()

    return cohort.cohort_id


def add_cohort_manager(s: Session, cohort_id: int, manager_id: int) -> int:
    cohort_manager = CohortManager(
        cohort_id=cohort_id,
        manager_id=manager_id,
    )

    s.add(cohort_manager)
    s.flush()

    return cohort_manager.cohort_manager_id


def add_student_cohort(s: Session, student_id: int, cohort_id: int) -> int:
    student_cohort = StudentCohort(
        student_id=student_id,
        cohort_id=cohort_id,
    )

    s.add(student_cohort)
    s.flush()

    return student_cohort.student_cohort_id


def add_student(
    s: Session,
    affiliation_id: int,
    program_id: int,
    date_start: date,
    date_end: date | None = None,
) -> int:
    fake_person = PersonProvider()

    student = Student(
        affiliation_id=affiliation_id,
        program_id=program_id,
        email_internal=fake_person.email(),
        date_start=date_start,
    )

    if date_end:
        student.date_end = date_end

    s.add(student)
    s.flush()

    return student.student_id


def demo():
    with Session(engine) as s:
        branch_id = add_branch(s)
        program_id = add_program(s, get_random_date())
        add_program_branch(s, program_id, branch_id)

        module_id = add_module(s, "PROGRAM", branch_id, get_random_date())
        course_id = add_course(s, module_id, get_random_date())

        person_id = add_person(s)
        teacher_id = add_employee(s, person_id, "TEACHER", "CONSULTANT", get_random_date())
        add_course_teacher(s, course_id, teacher_id)

        cohort_id = add_cohort(s, program_id, get_random_date())

        person_id = add_person(s)
        manager_id = add_employee(s, person_id, "MANAGER", "FULL_TIME", get_random_date())
        add_cohort_manager(s, cohort_id, manager_id)

        person_id = add_person(s)
        student_id = add_student(s, add_affiliation(s, person_id, "STUDENT"), program_id, get_random_date())
        add_student_cohort(s, student_id, cohort_id)


def main():
    DATE_HT = date(2025, 8, 18)
    DATE_HT_END = date(2025, 12, 28)
    DATE_HT24_VT26 = {"date_start": date(2024, 8, 26), "date_end": date(2026, 5, 31)}

    BRANCHES = {"STI Liljeholmen": "Stockholm", "STI Nordstan": "Göteborg"}

    PROGRAMS_COURSES = {
        "Data Engineer": {"SQL", "Data modelling", "Programmering inom data platform development"},
        "UX-designer": {"Interaktionsdesign", "Frontend", "UX research, tjänstedesign och användbarhetstestning"},
        "Systemutvecklare Inbyggda system": {
            "Digitalteknik och elektronik",
            "Objektorienterad programmering och design",
            "Algoritmer, datastrukturer och design patterns",
        },
        "Javautvecklare": {"Java Enterprise och Eclipse", "Testdriven utveckling", "Molntjänster"},
        "iOS/Android Developer": {
            "Hybridutveckling med Javascript 1",
            "OOP, datastrukturer, algoritmer och design",
            "Webbkommunikation, APIer och backend",
        },
    }

    with Session(engine) as s:
        # Add all programs
        for program_name in PROGRAMS_COURSES.keys():
            add_program(s, DATE_HT24_VT26["date_start"], DATE_HT24_VT26["date_end"], name=program_name)

        # Add branches
        for branch_name, city in BRANCHES.items():
            branch_id = add_branch(s, name=branch_name, city=city)

            # Add 3 random programs to each branch
            programs = s.execute(select(Program.program_id, Program.name)).all()

            for program_id, program_name in random.sample(programs, 3):
                add_program_branch(s, program_id, branch_id)

                # Add a module
                module_id = add_module(s, "PROGRAM", branch_id, DATE_HT, DATE_HT_END)
                add_module_program(s, module_id, program_id)

                # Add courses to module
                for course_name in PROGRAMS_COURSES[program_name]:
                    add_course(s, module_id, get_random_date_interval(DATE_HT, DATE_HT_END), name=course_name)

        # Add one teacher to each course in a module
        for module_id in s.scalars(select(Module.module_id)).all():
            teacher_id = add_employee(
                s,
                add_person(s),
                "TEACHER",
                random.choice(["FULL_TIME", "CONSULTANT"]),
                DATE_HT24_VT26["date_start"],
                DATE_HT24_VT26["date_end"],
            )

            # Add teacher to each course
            courses_ids = s.scalars(select(Course.course_id).where(Course.module_id == module_id)).all()
            for course_id in courses_ids:
                add_course_teacher(s, course_id, teacher_id)

        # Add student cohorts for each program at each branch
        programs_branches = s.scalars(select(ProgramBranch)).all()
        for program_branch in programs_branches:
            add_cohort(
                s,
                program_branch.program_id,
                program_branch.branch_id,
                DATE_HT24_VT26["date_start"],
                DATE_HT24_VT26["date_end"],
            )

        # Add manager to each cohort (max 3 cohorts per manager)
        cohorts_ids = s.scalars(select(Cohort.cohort_id)).all()
        for batch_cohorts in batched(cohorts_ids, 3):
            manager_id = add_employee(
                s,
                add_person(s),
                "MANAGER",
                random.choice(["FULL_TIME", "CONSULTANT"]),
                DATE_HT24_VT26["date_start"],
                DATE_HT24_VT26["date_end"],
            )
            for cohort_id in batch_cohorts:
                add_cohort_manager(s, cohort_id, manager_id)

        # Add 40 students to each cohort, add each student to one program
        for cohort_id in cohorts_ids:
            cohort_program_id = s.scalar(select(Cohort.program_id).where(Cohort.cohort_id == cohort_id))

            for _ in range(40):
                student_id = add_student(
                    s,
                    add_affiliation(s, add_person(s), "STUDENT"),
                    cohort_program_id,
                    DATE_HT24_VT26["date_start"],
                    DATE_HT24_VT26["date_end"],
                )
                add_student_cohort(s, student_id, cohort_id)

        # And voilà!
        s.commit()


if __name__ == "__main__":
    main()
