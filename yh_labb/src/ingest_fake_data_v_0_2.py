from datetime import date, datetime, timedelta
import random

from seed import BRANCHES

from mimesis import Generic
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL, Engine, create_engine, select, insert
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


SETTINGS = Settings()


POSTGRES_URL = URL.create(
    drivername="postgresql+psycopg",
    username=SETTINGS.postgres.user,
    password=SETTINGS.postgres.password.get_secret_value(),
    host=SETTINGS.postgres.host,
    port=SETTINGS.postgres.port,
    database=SETTINGS.postgres.dbname,
)


def get_random_date() -> datetime.date:
    return date(datetime.now().year, 1, 1) + timedelta(days=random.randint(0, 364))


def get_random_date_interval(date_start: date, date_end: date) -> datetime.date:
    return date_start + timedelta(days=random.randint(0, (date_end - date_start).days))


class DataIngestion:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.Base: AutomapBase = automap_base()
        self.Base.prepare(
            autoload_with=self.engine,
            schema=SETTINGS.database.dbschema,
        )

        # Main enteties
        self.Person = self.Base.classes.person
        self.AffiliationRole = self.Base.classes.affiliation_role
        self.Affiliation = self.Base.classes.affiliation

        self.EmploymentCategory = self.Base.classes.employment_category
        self.Employment = self.Base.classes.employment
        self.Consultant = self.Base.classes.consultant
        self.FullTime = self.Base.classes.full_time

        self.Manager = self.Base.classes.manager
        self.Teacher = self.Base.classes.teacher

        self.Branch = self.Base.classes.branch
        self.Program = self.Base.classes.program

        self.ModuleType = self.Base.classes.module_type
        self.Module = self.Base.classes.module
        self.Course = self.Base.classes.course

        self.Cohort = self.Base.classes.cohort
        self.Student = self.Base.classes.student

        # Junction tables
        self.ProgramBranch = self.Base.classes.program_branch
        self.ModuleProgram = self.Base.classes.module_program
        self.CourseModule = self.Base.classes.course_module

        self.TeacherCourse = self.Base.classes.teacher_course
        self.StudentCourse = self.Base.classes.student_course

        self.CohortManager = self.Base.classes.cohort_manager
        self.StudentCohort = self.Base.classes.student_cohort

        # Mimesis fake data provider
        self._fake = Generic()

    def ingest(self):
        with Session(self.engine) as s:
            self._ingest_branches(s)

    def _ingest_branches(self, s: Session):
        seed_branches = [
            {
                "name": seed_branch["name"],
                "city": seed_branch["city"],
                "address": self._fake.address.address(),
                "description": self._fake.text.sentence(),
            }
            for seed_branch in BRANCHES
        ]
        s.execute(insert(self.Branch), seed_branches)


def main():
    engine = create_engine(POSTGRES_URL)
    di = DataIngestion(engine)
    di.ingest()


if __name__ == "__main__":
    main()
