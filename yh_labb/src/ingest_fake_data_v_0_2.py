from datetime import date, datetime, timedelta
# from itertools import batched
# from typing import Literal
import random

# from mimesis.providers.address import Address as AddressProvider
# from mimesis.providers.finance import Finance as FinanceProvider
# from mimesis.providers.person import Person as PersonProvider
# from mimesis.random import Random as MimesisRandom


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


def main():
    with Session(engine) as s:
        pass


if __name__ == "__main__":
    main()
