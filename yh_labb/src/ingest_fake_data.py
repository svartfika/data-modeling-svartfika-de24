from pprint import pprint
import random
from typing import Literal

from mimesis.providers.person import Person as PersonProvider
from mimesis.providers.address import Address as AddressProvider
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
    affiliation_role_name: Literal["EMPLOYEE", "STUDENT"] | None = None,
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
        select(Affiliation.affiliation_role_id).where(
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


with Session(engine) as s:
    inspector = inspect(engine)

    person_id = add_person(s)
    add_affiliation(s, person_id, affiliation_role_name="EMPLOYEE")