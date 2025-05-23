from datetime import date, timedelta
import itertools
import random
from typing import Literal

from seed_data import BRANCHES, PROGRAMS_COURSES, SEMESTERS

from mimesis import Generic
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy import URL, Engine, and_, case, create_engine, insert, select, update
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
        self.ProgramCourse = self.Base.classes.program_course

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
            self._ingest_techers(s)
            self._ingest_cohorts(s)
            self._ingest_managers(s)
            self._ingest_students(s)
            self._ingest_student_course_junction(s)
            self._ingest_grades(s)
            s.commit()

    def _ingest_branches(self, s: Session):
        values = [
            {
                "name": seed_data["name"],
                "city": seed_data["city"],
                "address": self._fake.address.address(),
            }
            for seed_data in BRANCHES
        ]

        s.execute(insert(self.Branch), values)

    def _ingest_programs_courses(self, s: Session):
        # ingest programs

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
            insert(self.Program).returning(self.Program.program_id, self.Program.code), values_programs
        )

        programs_map = {code: id for id, code in result_programs.all()}

        # ingest courses

        course_program_map = {}
        values_courses = []

        for seed_data in PROGRAMS_COURSES:
            program_id = programs_map[seed_data["code"]]

            for course in seed_data["courses"]:
                course_code = course["code"]
                values_courses.append(
                    {
                        "name": course["name"],
                        "code": course_code,
                        "credits": self._fake.random.randint(10, 100),
                        "description": self._fake.text.sentence(),
                    }
                )
                course_program_map[course_code] = program_id

        result_courses = s.execute(
            insert(self.Course).returning(self.Course.course_id, self.Course.code), values_courses
        )

        # ingest program course junction table

        values_junction = []
        for course_id, course_code in result_courses:
            program_id = course_program_map.get(course_code)
            values_junction.append(
                {
                    "program_id": program_id,
                    "course_id": course_id,
                }
            )

        s.execute(insert(self.ProgramCourse), values_junction)

    def _ingest_program_branch_junction(self, s: Session):
        # ingest 3 random programs to program many-to-many branch junction table

        result_branch_ids = s.scalars(select(self.Branch.branch_id).where(self.Branch.name != "ONLINE")).all()

        values_junction = []
        for branch_id in result_branch_ids:
            result_program_ids = s.scalars(select(self.Program.program_id)).all()
            for program_id in random.sample(result_program_ids, 3):
                values_junction.append(
                    {
                        "program_id": program_id,
                        "branch_id": branch_id,
                        "date_start": SEMESTERS["HT24"]["date_start"],
                        "date_end": SEMESTERS["VT26"]["date_end"],
                    }
                )

        s.execute(insert(self.ProgramBranch), values_junction)

    def _ingest_modules_semesters(self, s: Session):
        # ingest modules

        module_type_name_map = self._create_lookup_map(s, self.ModuleType, value_field="module_type_id")

        result_branch_program = s.execute(
            select(self.Branch, self.Program)
            .join(self.ProgramBranch, self.Branch.branch_id == self.ProgramBranch.branch_id)
            .join(self.Program, self.Program.program_id == self.ProgramBranch.program_id)
        ).all()

        for branch, program in result_branch_program:
            result_program_course = s.scalars(
                select(self.Course)
                .join(self.ProgramCourse, self.Course.course_id == self.ProgramCourse.course_id)
                .where(self.ProgramCourse.program_id == program.program_id)
            ).all()

            values_semester = []
            for semster_code, date_range in SEMESTERS.items():
                values_semester.append(
                    {
                        "module_type_id": module_type_name_map["SEMESTER"],
                        "branch_id": branch.branch_id,
                        "name": f"{program.name} - {branch.city} - {semster_code}",
                        "code": f"{program.code}{date_range['date_start']:%y}-{branch.city}-{semster_code}",
                        "description": self._fake.text.sentence(),
                        "date_start": date_range["date_start"],
                        "date_end": date_range["date_end"],
                    }
                )

            result_modules = s.execute(insert(self.Module).returning(self.Module), values_semester).scalars().all()

            # ingest module program junction table

            values_module_program = [
                {
                    "module_id": module.module_id,
                    "program_id": program.program_id,
                    "date_start": module.date_start,
                    "date_end": module.date_end,
                }
                for module in result_modules
            ]

            s.execute(insert(self.ModuleProgram), values_module_program)

            # ingest course module junction table

            result_modules_ids = [r.module_id for r in result_modules]

            values_course_module = []
            for value_module_id, value_semster in zip(result_modules_ids, values_semester):
                course_intervals = self._divide_date_interval(
                    value_semster["date_start"], value_semster["date_end"], len(result_program_course)
                )

                for course, (date_start, date_end) in zip(result_program_course, course_intervals):
                    seed_course_module = {
                        "course_id": course.course_id,
                        "module_id": value_module_id,
                        "date_start": date_start,
                        "date_end": date_end,
                    }
                    values_course_module.append(seed_course_module)

            s.execute(insert(self.CourseModule), values_course_module)

    def _ingest_person(self, s: Session, n_persons: int = 1):
        values_person = [
            {
                "last_name": self._fake.person.last_name(),
                "first_name": self._fake.person.first_name(),
                "identity_number": f"{self._fake.person.birthdate().strftime('%Y%m%d')}-{self._fake.person.identifier('####')}",
                "address": self._fake.address.address(),
                "phone": self._fake.person.phone_number(),
                "email_private": self._fake.person.email(),
            }
            for _ in range(n_persons)
        ]

        result_person_ids = (
            s.execute(insert(self.Person).returning(self.Person.person_id), values_person).scalars().all()
        )

        return result_person_ids

    def _ingest_employee(
        self,
        s: Session,
        affiliation_role_name: Literal["EMPLOYEE", "MANAGER", "TEACHER"],
        date_start: date,
        # date_end: date | None = None,
        n_employees: int = 1,
    ):
        # ingest person(s)

        result_persons_ids = self._ingest_person(s, n_employees)

        # ingest affiliation

        affiliation_role_map = self._create_lookup_map(s, self.AffiliationRole, value_field="affiliation_role_id")

        values_affiliation = [
            {
                "person_id": person_id,
                "affiliation_role_id": affiliation_role_map[affiliation_role_name],
                "date_start": date_start,
                # "date_end": None,
            }
            for person_id in result_persons_ids
        ]

        result_affiliations_ids = (
            s.execute(insert(self.Affiliation).returning(self.Affiliation.affiliation_id), values_affiliation)
            .scalars()
            .all()
        )

        # ingest employment

        employment_category_id_map = self._create_lookup_map(
            s, self.EmploymentCategory, value_field="employment_category_id"
        )

        values_employment = [
            {
                "affiliation_id": affiliation_id,
                "employment_category_id": employment_category_id_map[
                    self._fake.random.choice(["CONSULTANT", "FULL_TIME"])
                ],
                "date_start": date_start,
                # "date_end": None,
            }
            for affiliation_id in result_affiliations_ids
        ]

        result_employments_ids = (
            s.execute(insert(self.Employment).returning(self.Employment.employment_id), values_employment)
            .scalars()
            .all()
        )

        # ingest employment category data, employment role

        employment_category_name_map = self._create_lookup_map(
            s, self.EmploymentCategory, key_field="employment_category_id", value_field="name"
        )

        values_consultant = []
        values_full_time = []
        values_manager = []
        values_teacher = []

        for employment_id, value_employment in zip(result_employments_ids, values_employment):
            employment_category_id = employment_category_name_map.get(value_employment["employment_category_id"])

            if employment_category_id == "CONSULTANT":
                values_consultant.append(
                    {
                        "employment_id": employment_id,
                        "org_name": self._fake.finance.company(),
                        "org_number": self._fake.random.generate_string_by_mask("######-####"),
                        "f_skatt": self._fake.development.boolean(),
                        "rate_hourly": self._fake.random.randint(500, 1500),
                    }
                )
            elif employment_category_id == "FULL_TIME":
                values_full_time.append(
                    {
                        "employment_id": employment_id,
                        "salary_monthly": self._fake.random.randint(25000, 55000),
                        "hours_weekly": self._fake.random.randint(20, 40),
                    }
                )

            if affiliation_role_name == "MANAGER":
                values_manager.append({"employment_id": employment_id})
            elif affiliation_role_name == "TEACHER":
                values_teacher.append({"employment_id": employment_id})

        if values_consultant:
            s.execute(insert(self.Consultant), values_consultant)
        if values_full_time:
            s.execute(insert(self.FullTime), values_full_time)

        if values_manager:
            return s.execute(insert(self.Manager).returning(self.Manager.manager_id), values_manager).scalars().all()
        if values_teacher:
            return s.execute(insert(self.Teacher).returning(self.Teacher.teacher_id), values_teacher).scalars().all()

    def _ingest_techers(self, s: Session, n_teachers_max: int = 1):
        # query for all relevant data

        result_branch_program_module_course = s.execute(
            select(
                self.Branch,
                self.Program,
                self.ProgramBranch,
                self.CourseModule,
            )
            .join_from(self.Branch, self.ProgramBranch, self.Branch.branch_id == self.ProgramBranch.branch_id)
            .join(self.Program, self.Program.program_id == self.ProgramBranch.program_id)
            .join(self.Module, self.Module.branch_id == self.Branch.branch_id)
            .join(self.CourseModule, self.CourseModule.module_id == self.Module.module_id)
            .join(
                self.ProgramCourse,
                and_(
                    self.ProgramCourse.course_id == self.CourseModule.course_id,
                    self.ProgramCourse.program_id == self.Program.program_id,
                ),
            )
        ).all()

        # iterate over branch-program

        branch_program_pairs = {
            (row[0], row[1], row[2].date_start, row[2].date_end) for row in result_branch_program_module_course
        }

        for branch, program, program_date_start, program_date_end in branch_program_pairs:
            # ingest n teacher(s)

            n_teachers = random.randint(1, n_teachers_max)
            result_teachers_ids = self._ingest_employee(s, "TEACHER", program_date_start, n_employees=n_teachers)

            # ingest teacher many-to-many course junction table

            courses_ids = [
                (row[3].course_module_id, row[3].date_start)
                for row in result_branch_program_module_course
                if row[0].branch_id == branch.branch_id and row[1].program_id == program.program_id
            ]

            values_teacher_course_module_ids = [
                {
                    "teacher_id": teacher_id,
                    "course_module_id": course_module_id,
                    "date_start": date_start,
                }
                for teacher_id, (course_module_id, date_start) in zip(itertools.cycle(result_teachers_ids), courses_ids)
            ]

            s.execute(insert(self.TeacherCourse), values_teacher_course_module_ids)

    def _ingest_cohorts(self, s: Session):
        # ingest cohorts for each program at each branch

        result_program_branch = s.execute(
            select(self.Branch, self.Program, self.ProgramBranch)
            .join_from(self.Branch, self.ProgramBranch, self.Branch.branch_id == self.ProgramBranch.branch_id)
            .join(self.Program, self.Program.program_id == self.ProgramBranch.program_id)
        ).all()

        values_cohort = []
        for branch, program, program_branch in result_program_branch:
            values_cohort.append(
                {
                    "program_id": program_branch.program_id,
                    "branch_id": program_branch.branch_id,
                    "name": f"{program.name} - {branch.city} - {program_branch.date_start:%Y}",
                    "code": f"{program.code}{program_branch.date_start:%y}-{branch.city}",
                    "date_start": program_branch.date_start,
                    "date_end": program_branch.date_end,
                }
            )

        s.execute(insert(self.Cohort), values_cohort)

    def _ingest_managers(self, s: Session, n_courses_max: int = 3):
        values_cohort_manager = []

        result_cohort = (
            s.execute(
                select(self.Cohort).order_by(
                    self.Cohort.branch_id,
                    self.Cohort.program_id,
                    self.Cohort.date_start,
                )
            )
            .scalars()
            .all()
        )

        # iterate of branch-cohort

        for branch_id in {r.branch_id for r in result_cohort}:
            branch_cohorts = [r for r in result_cohort if r.branch_id == branch_id]

            for batch_cohort in itertools.batched(branch_cohorts, n_courses_max):
                # ingest manager for each batch of n_courses_max cohorts

                result_manager_id = self._ingest_employee(s, "MANAGER", batch_cohort[0].date_start)

                # ingest cohort many-to-many manager junction table

                for cohort in batch_cohort:
                    values_cohort_manager.append(
                        {
                            "cohort_id": cohort.cohort_id,
                            "manager_id": result_manager_id[0],
                            "date_start": cohort.date_start,
                            "date_end": cohort.date_end,
                        }
                    )

        s.execute(insert(self.CohortManager), values_cohort_manager)

    def _ingest_students(self, s: Session, n_cohort_max: int = 45):
        result_cohort = s.execute(select(self.Cohort)).scalars().all()
        cycle_result_cohort = itertools.cycle(result_cohort)

        # ingest n_cohort_max persons per cohort

        result_persons_ids = self._ingest_person(s, n_cohort_max * len(result_cohort))

        # ingest affiliation

        affiliation_role_map = self._create_lookup_map(s, self.AffiliationRole, value_field="affiliation_role_id")

        values_affiliation = [
            {
                "person_id": person_id,
                "affiliation_role_id": affiliation_role_map["STUDENT"],
                "date_start": cohort.date_start,
                "date_end": cohort.date_end,
            }
            for cohort, person_id in zip(cycle_result_cohort, result_persons_ids)
        ]

        result_affiliation = (
            s.execute(insert(self.Affiliation).returning(self.Affiliation), values_affiliation).scalars().all()
        )

        # ingest students

        values_student = [
            {
                "affiliation_id": affiliation.affiliation_id,
                "email_internal": self._fake.person.email(),
                "date_start": affiliation.date_start,
                "date_end": affiliation.date_end,
            }
            for cohort, affiliation in zip(cycle_result_cohort, result_affiliation)
        ]

        result_student = s.execute(insert(self.Student).returning(self.Student), values_student).scalars().all()

        # ingest student cohort junction table

        values_student_cohort = [
            {
                "student_id": student.student_id,
                "cohort_id": cohort.cohort_id,
                "date_start": cohort.date_start,
                "date_end": cohort.date_end,
            }
            for cohort, student in zip(cycle_result_cohort, result_student)
        ]

        s.execute(insert(self.StudentCohort), values_student_cohort)

    def _ingest_student_course_junction(self, s: Session):
        # query courses by module, match to student's program-branch

        result_cohort_courses = s.execute(
            select(
                self.StudentCohort.student_id,
                self.CourseModule,
            )
            .join_from(self.CourseModule, self.Module, self.CourseModule.module_id == self.Module.module_id)
            .join(self.ModuleProgram, self.Module.module_id == self.ModuleProgram.module_id)
            .join(self.Cohort, self.Module.branch_id == self.Cohort.branch_id)
            .where(self.Cohort.program_id == self.ModuleProgram.program_id)
            .join(self.StudentCohort, self.Cohort.cohort_id == self.StudentCohort.cohort_id)
            .order_by(self.StudentCohort.student_id, self.CourseModule.course_module_id)
        ).all()

        # ingest student course junction table

        values_student_course = [
            {
                "student_id": student_id,
                "course_module_id": course.course_module_id,
                "date_start": course.date_start,
                "date_end": course.date_end,
            }
            for student_id, course in result_cohort_courses
        ]

        s.execute(insert(self.StudentCourse), values_student_course)

    def _ingest_grades(self, s: Session):
        result_student_course = s.execute(select(self.StudentCourse.student_course_id)).scalars().all()

        # ingest grades in chunks

        chunk_size = 1000
        for i in range(0, len(result_student_course), chunk_size):
            chunk_ids = result_student_course[i : i + chunk_size]

            # prepare case statement to match each row

            values_whens = []
            for student_course_id, grade_code in zip(chunk_ids, self._grade_generator(chunk_size)):
                values_whens.append((self.StudentCourse.student_course_id == student_course_id, grade_code))

            s.execute(
                update(self.StudentCourse)
                .where(self.StudentCourse.student_course_id.in_(chunk_ids))
                .values(grade_code=case(*values_whens))
                .execution_options(synchronize_session=False)
            )

    def _create_lookup_map(self, s: Session, model_class, key_field="name", value_field="id") -> dict:
        return {getattr(obj, key_field): getattr(obj, value_field) for obj in s.scalars(select(model_class)).all()}

    def _divide_date_interval(self, start_date: date, end_date: date, x: int):
        interval = (end_date - start_date).days / x
        return [
            (
                start_date + timedelta(days=int(interval * i)),
                end_date if i == x - 1 else start_date + timedelta(days=int(interval * (i + 1))),
            )
            for i in range(x)
        ]

    def _grade_generator(self, count: int | None = None):
        i = 0
        while count is None or i < count:
            yield self._fake.random.weighted_choice({"IG": 0.1, "G": 0.6, "VG": 0.3})
            i += 1


def main():
    engine = create_engine(POSTGRES_URL)
    genrate_fake_data = DataIngestion(engine)
    genrate_fake_data.ingest()


if __name__ == "__main__":
    main()
