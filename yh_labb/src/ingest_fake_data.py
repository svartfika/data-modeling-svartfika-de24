from datetime import date, datetime, timedelta
from pprint import pprint
import random
from typing import Literal

from mimesis.providers.address import Address as AddressProvider
from mimesis.providers.finance import Finance as FinanceProvider
from mimesis.random import Random as MimesisRandom
from mimesis.providers.person import Person as PersonProvider


from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL, create_engine, inspect, select
from sqlalchemy.ext.automap import automap_base, AutomapBase
from sqlalchemy.orm import Session


class PostgresSettings(BaseSettings):
    host: str = Field(default="127.0.0.1")
    port: int = Field(default="5432")
    user: str = Field(default="postgres")
    password: SecretStr = Field(default_factory=lambda: SecretStr(""))
    dbname: str = Field(default="postgres_db")

    # model_config = SettingsConfigDict(env_prefix="POSTGRES_")


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
    *,
    affiliation_role_id: int | None = None,
    affiliation_role_name: Literal["EMPLOYEE", "MANAGER", "STUDENT", "TEACHER"] | None = None,
) -> int:
    if affiliation_role_name:
        role_id = s.scalar(
            select(AffiliationRole.affiliation_role_id).where(AffiliationRole.name == affiliation_role_name)
        )

        if not role_id:
            raise KeyError(f"affiliation_role_name '{affiliation_role_name}' not found")

    elif affiliation_role_id:
        role_id = s.scalar(
            select(AffiliationRole.affiliation_role_id).where(
                AffiliationRole.affiliation_role_id == affiliation_role_id
            )
        )

        if not role_id:
            raise KeyError(f"affiliation_role_id '{affiliation_role_id}' not found")

    else:
        raise ValueError("'affiliation_role_id' or 'affiliation_role_name' must be provided")

    exists_id = s.scalar(
        select(Affiliation.affiliation_id).where(
            Affiliation.person_id == person_id,
            Affiliation.affiliation_role_id == role_id,
        )
    )

    if exists_id:
        return exists_id

    affiliation = Affiliation(person_id=person_id, affiliation_role_id=role_id)

    s.add(affiliation)
    s.flush()

    return affiliation.affiliation_id


def add_employment(
    s: Session,
    affiliation_id: int,
    *,
    employment_category_id: int | None = None,
    employment_category_name: Literal["CONSULTANT", "FULL_TIME"] | None = None,
    date_start: date | None = None,
    date_end: date | None = None,
) -> int:
    if employment_category_name:
        category_id = s.scalar(
            select(EmploymentCategory.employment_category_id).where(EmploymentCategory.name == employment_category_name)
        )

        if not category_id:
            raise KeyError(f"affiliation_role_name '{employment_category_name}' not found")

    elif employment_category_id:
        category_id = s.scalar(
            select(EmploymentCategory.employment_category_id).where(
                EmploymentCategory.employment_category_id == employment_category_id
            )
        )

        if not category_id:
            raise KeyError(f"employment_category_id '{employment_category_id}' not found")

    else:
        raise ValueError("'employment_category_id' or 'employment_category_name' must be provided")

    if not date_start:
        date_start = get_random_date()

    exists_id = s.scalar(
        select(Employment.employment_id).where(
            Employment.affiliation_id == affiliation_id,
            Employment.employment_category_id == category_id,
            Employment.date_start == date_start,
        )
    )

    if exists_id:
        return exists_id

    employment = Employment(
        affiliation_id=affiliation_id,
        employment_category_id=category_id,
        date_start=date_start,
    )

    s.add(employment)
    s.flush()

    return employment.employment_id


def add_consultant(s: Session, employment_id: int) -> int:
    exists_id = s.scalar(select(Employment.employment_id).where(Employment.employment_id == employment_id))
    if not exists_id:
        raise KeyError(f"employment_id '{employment_id}' not found")

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
    exists_id = s.scalar(select(Employment.employment_id).where(Employment.employment_id == employment_id))
    if not exists_id:
        raise KeyError(f"employment_id '{employment_id}' not found")

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
    exists_id = s.scalar(select(Employment.employment_id).where(Employment.employment_id == employment_id))
    if not exists_id:
        raise KeyError(f"employment_id '{employment_id}' not found")

    manager = Manager(employment_id=employment_id)

    s.add(manager)
    s.flush()

    return manager.manager_id


def add_teacher(s: Session, employment_id: int) -> int:
    exists_id = s.scalar(select(Employment.employment_id).where(Employment.employment_id == employment_id))
    if not exists_id:
        raise KeyError(f"employment_id '{employment_id}' not found")

    teacher = Teacher(employment_id=employment_id)

    s.add(teacher)
    s.flush()

    return teacher.teacher_id


def add_employee(
    s: Session,
    person_id: int,
    affiliation_role_name: Literal["EMPLOYEE", "MANAGER", "TEACHER"],
    employment_category_name: Literal["CONSULTANT", "FULL_TIME"],
) -> int:
    exists_id = s.scalar(select(Person.person_id).where(Person.person_id == person_id))
    if not exists_id:
        raise KeyError(f"person_id '{person_id}' not found")

    affiliation_id = add_affiliation(s, person_id, affiliation_role_name=affiliation_role_name)
    employment_id = add_employment(s, affiliation_id, employment_category_name=employment_category_name)

    if affiliation_role_name == "MANAGER":
        add_manager(s, employment_id)
    elif affiliation_role_name == "TEACHER":
        add_teacher(s, employment_id)
    else:
        raise KeyError(f"affiliation_role_name '{affiliation_role_name}' not found")

    if employment_category_name == "CONSULTANT":
        add_consultant(s, employment_id)
    elif employment_category_name == "FULL_TIME":
        add_full_time(s, employment_id)
    else:
        raise KeyError(f"employment_category_name '{employment_category_name}' not found")

    return employment_id


if __name__ == "__main__":
    with Session(engine) as s:
        inspector = inspect(engine)

        person_id = add_person(s)
        affiliation_id = add_affiliation(s, person_id, affiliation_role_name="TEACHER")
        employment_id = add_employment(s, affiliation_id, employment_category_name="CONSULTANT")
        consultant_id = add_consultant(s, employment_id)
        manager_id = add_manager(s, employment_id)

        person_id = add_person(s)
        affiliation_id = add_affiliation(s, person_id, affiliation_role_name="MANAGER")
        employment_id = add_employment(s, affiliation_id, employment_category_name="FULL_TIME")
        full_time_id = add_full_time(s, employment_id)
        teacher_id = add_teacher(s, employment_id)

        person_id = add_person(s)
        employment_id = add_employee(s, person_id, "MANAGER", "FULL_TIME")

        person_id = add_person(s)
        employment_id = add_employee(s, person_id, "TEACHER", "CONSULTANT")
