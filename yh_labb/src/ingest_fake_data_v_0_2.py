from datetime import date, datetime, timedelta
import random

from seed_data import BRANCHES, PROGRAMS_COURSES, SEMESTERS

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


def random_date_this_year() -> datetime.date:
    return date(datetime.now().year, 1, 1) + timedelta(days=random.randint(0, 364))


def random_date_between(date_start: date, date_end: date) -> datetime.date:
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
            self._ingest_programs_courses(s)
            self._ingest_program_branch_junction(s)
            self._ingest_modules_semesters(s)

    def _ingest_branches(self, s: Session):
        values = [
            {
                "name": seed_data["name"],
                "city": seed_data["city"],
                "address": self._fake.address.address(),
                "description": self._fake.text.sentence(),
            }
            for seed_data in BRANCHES
        ]

        s.execute(insert(self.Branch), values)

    def _ingest_programs_courses(self, s: Session):
        values_courses = []
        values_programs = [
            {
                "name": seed_data["name"],
                "code": seed_data["code"],
                "cycle": self._fake.random.randint(1, 3),
                "description": self._fake.text.sentence(),
            }
            for seed_data in PROGRAMS_COURSES
        ]

        result_programs = s.execute(
            insert(self.Program).returning(self.Program.program_id, self.Program.code),
            values_programs,
        )

        programs_map = {code: id for id, code in result_programs.all()}

        for seed_data in PROGRAMS_COURSES:
            program_id = programs_map[seed_data["code"]]
            for course in seed_data["courses"]:
                seed_course = {
                    "program_id": program_id,
                    "name": course["name"],
                    "code": course["code"],
                    "credits": self._fake.random.randint(10, 100),
                    "description": self._fake.text.sentence(),
                }
                values_courses.append(seed_course)

        s.execute(
            insert(self.Course),
            values_courses,
        )

    def _ingest_program_branch_junction(self, s: Session):
        values_junction = []

        for branch_id in s.scalars(select(self.Branch.branch_id)).all():
            for program_id in s.scalars(select(self.Program.program_id)).all():
                seed_junction = {
                    "program_id": program_id,
                    "branch_id": branch_id,
                    "date_start": SEMESTERS["HT24"]["date_start"],
                    "date_end": SEMESTERS["VT26"]["date_end"],
                }
                values_junction.append(seed_junction)

        s.execute(
            insert(self.ProgramBranch),
            values_junction,
        )

    def _ingest_modules_semesters(self, s: Session):
        module_types_map = {r.name: r.module_type_id for r in s.scalars(select(self.ModuleType)).all()}

        result_branch_program = s.execute(
            select(self.Branch, self.Program)
            .join(self.ProgramBranch, self.Branch.branch_id == self.ProgramBranch.branch_id)
            .join(self.Program, self.Program.program_id == self.ProgramBranch.program_id)
        ).all()

        for branch, program in result_branch_program:
            result_program_course = s.scalars(
                select(self.Course).where(self.Course.program_id == program.program_id)
            ).all()

            values_semester = []
            for semster_code, date_range in SEMESTERS.items():
                seed_semester = {
                    "module_type_id": module_types_map["SEMESTER"],
                    "branch_id": branch.branch_id,
                    "name": f"{program.name} - {program.code}{semster_code}",
                    "code": f"{program.code}{semster_code}",
                    "description": self._fake.text.sentence(),
                    "date_start": date_range["date_start"],
                    "date_end": date_range["date_end"],
                }

                values_semester.append((seed_semester, result_program_course))

            values_course_module = []
            for value_module, courses in values_semester:
                result_module_id = s.scalar(insert(self.Module).returning(self.Module.module_id), value_module)

                course_intervals = self.divide_date_interval(
                    value_module["date_start"], value_module["date_end"], len(courses)
                )

                for course, (date_start, date_end) in zip(courses, course_intervals):
                    seed_course_module = {
                        "course_id": course.course_id,
                        "module_id": result_module_id,
                        "date_start": date_start,
                        "date_end": date_end,
                    }
                    values_course_module.append(seed_course_module)

            s.execute(insert(self.CourseModule), values_course_module)

    def _divide_date_interval(start_date: date, end_date: date, x: int):
        interval = (end_date - start_date).days / x
        return [
            (
                start_date + timedelta(days=int(interval * i)),
                end_date if i == x - 1 else start_date + timedelta(days=int(interval * (i + 1))),
            )
            for i in range(x)
        ]


def main():
    engine = create_engine(POSTGRES_URL)
    di = DataIngestion(engine)
    di.ingest()


if __name__ == "__main__":
    main()
