## Uppgift 0 - datamodellering

### 0_d

> Skapa fysisk modell baserat pà den logiska modellen

#### Adding Dtypes

```mermaid
erDiagram



PERSON ||--o{ AFFILIATION : has
AffiliationRole ||--o{ AFFILIATION : defines
AFFILIATION ||--o{ EMPLOYEE : employs
AFFILIATION ||--o{ STUDENT : enrolls

EmployeeCategory ||--o{ EMPLOYEE : categorizes

PROGRAM ||--o{ STUDENT : enrolls
PROGRAM ||--o{ ProgramBranch : includes
BRANCH ||--o{ ProgramBranch : hosts

BRANCH ||--o{ EMPLOYEE : employs
BRANCH ||--o{ MODULE : hosts

ModuleType ||--o{ MODULE : classifies



EMPLOYEE ||--o| CONSULTANT : is
EMPLOYEE ||--o| FULL_TIME : is
EMPLOYEE ||--o| TEACHER : is
EMPLOYEE ||--o| MANAGER : is

MODULE ||--o{ ModuleProgram : includes
PROGRAM ||--o{ ModuleProgram : includes

MODULE ||--o{ COURSE : contains

STUDENT ||--o{ CourseStudent : takes
COURSE ||--o{ CourseStudent : has

TEACHER ||--o{ CourseTeacher : teaches
COURSE ||--o{ CourseTeacher : has

COHORT ||--o{ StudentCohort : groups
STUDENT ||--o{ StudentCohort : "belongs to"

MANAGER ||--o{ CohortManager : manages
COHORT ||--o{ CohortManager : has



PERSON {
  SERIAL person_id
  VARCHAR last_name
  VARCHAR first_name
  VARCHAR identity_number
  TEXT address
  VARCHAR phone
  VARCHAR email_private
}

AffiliationRole {
  SERIAL affiliation_role_id
  VARCHAR name
  TEXT description
}

AFFILIATION {
  SERIAL affiliation_id
  INTEGER person_id
  INTEGER affiliation_role_id
}

EmployeeCategory {
  SERIAL employee_category_id
  VARCHAR name
  TEXT description
}

EMPLOYEE {
  SERIAL employee_id
  INTEGER affiliation_id
  INTEGER employee_category_id
  DATE date_start
  DATE date_end
}

STUDENT {
  SERIAL student_id
  INTEGER affiliation_id
  INTEGER program_id
  VARCHAR email_internal
}

PROGRAM {
  SERIAL program_id
  VARCHAR name
  CHAR code
  INT cycle
  TEXT description
  DATE date_start
  DATE date_end
}

BRANCH {
  SERIAL branch_id
  VARCHAR name
  VARCHAR city
  TEXT address
}

ModuleType {
  SERIAL module_type_id
  VARCHAR name
  TEXT description
}

MODULE {
  SERIAL module_id
  INTEGER module_type_id
  INTEGER branch_id
  VARCHAR name
  CHAR code
  TEXT description
  DATE date_start
  DATE date_end
}

COURSE {
  SERIAL course_id
  INTEGER module_id
  VARCHAR name
  CHAR code
  INTEGER credits
  TEXT description
  DATE date_start
  DATE date_end
}

CONSULTANT {
  INTEGER employee_id
  VARCHAR org_name
  VARCHAR org_number
  BOOLEAN f_skatt
  TEXT address
  MONEY rate_hourly
}

FULL_TIME {
  INTEGER employee_id
  MONEY salary_monthly
  NUMERIC hours_weekly
}

TEACHER {
  SERIAL teacher_id
  INTEGER employee_id
}

MANAGER {
  SERIAL manager_id
  INTEGER employee_id
}

ProgramBranch {
  SERIAL program_branch_id
  INTEGER program_id
  INTEGER branch_id
}

ModuleProgram {
  SERIAL module_program_id
  INTEGER module_id
  INTEGER program_id
}

CourseTeacher {
  SERIAL course_teacher_id
  INTEGER course_id
  INTEGER teacher_id
}

CourseStudent {
  SERIAL course_student_id
  INTEGER course_id
  INTEGER student_id
}

COHORT {
  SERIAL cohort_id
}

StudentCohort {
  SERIAL cohort_student_id
  INTEGER cohort_id
  INTEGER student_id
}

CohortManager {
  SERIAL cohort_manager_id
  INTEGER cohort_id
  INTEGER manager_id
}
```

---

#### Adding primary/foreign keys

```mermaid
erDiagram



PERSON ||--o{ AFFILIATION : has
AffiliationRole ||--o{ AFFILIATION : defines
AFFILIATION ||--o{ EMPLOYEE : employs
AFFILIATION ||--o{ STUDENT : enrolls

EmployeeCategory ||--o{ EMPLOYEE : categorizes

PROGRAM ||--o{ STUDENT : enrolls
PROGRAM ||--o{ ProgramBranch : includes
BRANCH ||--o{ ProgramBranch : hosts

BRANCH ||--o{ EMPLOYEE : employs
BRANCH ||--o{ MODULE : hosts

ModuleType ||--o{ MODULE : classifies



EMPLOYEE ||--o| CONSULTANT : is
EMPLOYEE ||--o| FULL_TIME : is
EMPLOYEE ||--o| TEACHER : is
EMPLOYEE ||--o| MANAGER : is

MODULE ||--o{ ModuleProgram : includes
PROGRAM ||--o{ ModuleProgram : includes

MODULE ||--o{ COURSE : contains

STUDENT ||--o{ CourseStudent : takes
COURSE ||--o{ CourseStudent : has

TEACHER ||--o{ CourseTeacher : teaches
COURSE ||--o{ CourseTeacher : has

COHORT ||--o{ StudentCohort : groups
STUDENT ||--o{ StudentCohort : "belongs to"

MANAGER ||--o{ CohortManager : manages
COHORT ||--o{ CohortManager : has



PERSON {
  SERIAL person_id PK
  VARCHAR last_name
  VARCHAR first_name
  VARCHAR identity_number
  TEXT address
  VARCHAR phone
  VARCHAR email_private
}

AffiliationRole {
  SERIAL affiliation_role_id PK
  VARCHAR name
  TEXT description
}

AFFILIATION {
  SERIAL affiliation_id PK
  INTEGER person_id FK
  INTEGER affiliation_role_id FK
}

EmployeeCategory {
  SERIAL employee_category_id PK
  VARCHAR name
  TEXT description
}

EMPLOYEE {
  SERIAL employee_id PK
  INTEGER affiliation_id FK
  INTEGER employee_category_id FK
  DATE date_start
  DATE date_end
}

STUDENT {
  SERIAL student_id PK
  INTEGER affiliation_id FK
  INTEGER program_id FK
  VARCHAR email_internal
}

PROGRAM {
  SERIAL program_id PK
  VARCHAR name
  VARCHAR code
  INT cycle
  TEXT description
  DATE date_start
  DATE date_end
}

BRANCH {
  SERIAL branch_id PK
  VARCHAR name
  VARCHAR city
  TEXT address
}

ModuleType {
  SERIAL module_type_id PK
  VARCHAR name
  TEXT description
}

MODULE {
  SERIAL module_id PK
  INTEGER module_type_id FK
  INTEGER branch_id FK
  VARCHAR name
  VARCHAR code
  TEXT description
  DATE date_start
  DATE date_end
}

COURSE {
  SERIAL course_id PK
  INTEGER module_id FK
  VARCHAR name
  VARCHAR code
  INTEGER credits
  TEXT description
  DATE date_start
  DATE date_end
}

CONSULTANT {
  INTEGER employee_id FK
  VARCHAR org_name
  VARCHAR org_number
  BOOLEAN f_skatt
  MONEY rate_hourly
  TEXT address
}

FULL_TIME {
  INTEGER employee_id FK
  MONEY salary_monthly
  NUMERIC hours_weekly
}

TEACHER {
  SERIAL teacher_id PK
  INTEGER employee_id FK
}

MANAGER {
  SERIAL manager_id PK
  INTEGER employee_id FK
}

ProgramBranch {
  SERIAL program_branch_id PK
  INTEGER program_id FK
  INTEGER branch_id FK
}

ModuleProgram {
  SERIAL module_program_id PK
  INTEGER module_id FK
  INTEGER program_id FK
}

CourseTeacher {
  SERIAL course_teacher_id PK
  INTEGER course_id FK
  INTEGER teacher_id FK
}

CourseStudent {
  SERIAL course_student_id PK
  INTEGER course_id FK
  INTEGER student_id FK
}

COHORT {
  SERIAL cohort_id PK
}

StudentCohort {
  SERIAL cohort_student_id PK
  INTEGER cohort_id FK
  INTEGER student_id FK
}

CohortManager {
  SERIAL cohort_manager_id PK
  INTEGER cohort_id FK
  INTEGER manager_id FK
}
```

---

#### Adding Dtypes

```mermaid
erDiagram



PERSON ||--o{ AFFILIATION : has
AffiliationRole ||--o{ AFFILIATION : defines
AFFILIATION ||--o{ EMPLOYEE : employs
AFFILIATION ||--o{ STUDENT : enrolls

EmployeeCategory ||--o{ EMPLOYEE : categorizes

PROGRAM ||--o{ STUDENT : enrolls
PROGRAM ||--o{ ProgramBranch : includes
BRANCH ||--o{ ProgramBranch : hosts

BRANCH ||--o{ EMPLOYEE : employs
BRANCH ||--o{ MODULE : hosts

ModuleType ||--o{ MODULE : classifies

EMPLOYEE ||--o| CONSULTANT : is
EMPLOYEE ||--o| FULL_TIME : is
EMPLOYEE ||--o| TEACHER : is
EMPLOYEE ||--o| MANAGER : is

MODULE ||--o{ ModuleProgram : includes
PROGRAM ||--o{ ModuleProgram : includes

MODULE ||--o{ COURSE : contains

STUDENT ||--o{ CourseStudent : takes
COURSE ||--o{ CourseStudent : has

TEACHER ||--o{ CourseTeacher : teaches
COURSE ||--o{ CourseTeacher : has

COHORT ||--o{ StudentCohort : groups
STUDENT ||--o{ StudentCohort : "belongs to"

MANAGER ||--o{ CohortManager : manages
COHORT ||--o{ CohortManager : has



PERSON {
  SERIAL person_id
  VARCHAR last_name
  VARCHAR first_name
  VARCHAR identity_number
  TEXT address
  VARCHAR phone
  VARCHAR email_private
}

AffiliationRole {
  SERIAL affiliation_role_id
  VARCHAR name
  TEXT description
}

AFFILIATION {
  SERIAL affiliation_id
  INTEGER person_id
  INTEGER affiliation_role_id
}

EmployeeCategory {
  SERIAL employee_category_id
  VARCHAR name
  TEXT description
}

EMPLOYEE {
  SERIAL employee_id
  INTEGER affiliation_id
  INTEGER employee_category_id
  DATE date_start
  DATE date_end
}

STUDENT {
  SERIAL student_id
  INTEGER affiliation_id
  INTEGER program_id
  VARCHAR email_internal
}

PROGRAM {
  SERIAL program_id
  VARCHAR name
  CHAR code
  INT cycle
  TEXT description
  DATE date_start
  DATE date_end
}

BRANCH {
  SERIAL branch_id
  VARCHAR name
  VARCHAR city
  TEXT address
}

ModuleType {
  SERIAL module_type_id
  VARCHAR name
  TEXT description
}

MODULE {
  SERIAL module_id
  INTEGER module_type_id
  INTEGER branch_id
  VARCHAR name
  CHAR code
  TEXT description
  DATE date_start
  DATE date_end
}

COURSE {
  SERIAL course_id
  INTEGER module_id
  VARCHAR name
  CHAR code
  INTEGER credits
  TEXT description
  DATE date_start
  DATE date_end
}

CONSULTANT {
  INTEGER employee_id
  VARCHAR org_name
  VARCHAR org_number
  BOOLEAN f_skatt
  TEXT address
  MONEY rate_hourly
}

FULL_TIME {
  INTEGER employee_id
  MONEY salary_monthly
  NUMERIC hours_weekly
}

TEACHER {
  SERIAL teacher_id
  INTEGER employee_id
}

MANAGER {
  SERIAL manager_id
  INTEGER employee_id
}

ProgramBranch {
  SERIAL program_branch_id
  INTEGER program_id
  INTEGER branch_id
}

ModuleProgram {
  SERIAL module_program_id
  INTEGER module_id
  INTEGER program_id
}

CourseTeacher {
  SERIAL course_teacher_id
  INTEGER course_id
  INTEGER teacher_id
}

CourseStudent {
  SERIAL course_student_id
  INTEGER course_id
  INTEGER student_id
}

COHORT {
  SERIAL cohort_id
}

StudentCohort {
  SERIAL cohort_student_id
  INTEGER cohort_id
  INTEGER student_id
}

CohortManager {
  SERIAL cohort_manager_id
  INTEGER cohort_id
  INTEGER manager_id
}
```

---

#### Updates reflecting changes in init.sql

```mermaid
erDiagram
    person ||--o{ affiliation : has
    affiliation_role ||--o{ affiliation : defines
    affiliation ||--o{ student : is
    affiliation ||--o{ employment : is

    employment_category ||--o{ employment   : categorizes
    employment ||--o| consultant : is
    employment ||--o| full_time : is
    employment ||--o| teacher : is
    employment ||--o| manager : is

    program ||--o{ program_branch : includes
    branch ||--o{ program_branch : hosts
    branch ||--o{ module : hosts
    module_type ||--o{ module : classifies
    program ||--o{ module_program : includes
    module ||--o{ module_program : includes
    module ||--o{ course_module : contains
    course ||--o{ course_module : "belongs to"

    course_module ||--o{ student_course : enrolled
    student ||--o{ student_course : takes
    grade_type ||--o{ student_course : rates
    course_module ||--o{ teacher_course : assigned
    teacher ||--o{ teacher_course : teaches

    cohort ||--o{ student_cohort : groups
    student ||--o{ student_cohort : "belongs to"

    manager ||--o{ cohort_manager : manages
    cohort ||--o{ cohort_manager : has

    person {
        BIGINT person_id PK
        VARCHAR last_name "NOT NULL"
        VARCHAR first_name "NOT NULL"
        VARCHAR identity_number "NOT NULL"
        TEXT address "NOT NULL"
        VARCHAR phone "NOT NULL"
        VARCHAR email_private "NOT NULL"
        _ UNIQUE "(identity_number)"
    }

    affiliation_role {
        BIGINT affiliation_role_id PK
        VARCHAR name "NOT NULL"
        _ UNIQUE "(name)"
    }

    affiliation {
        BIGINT affiliation_id PK
        BIGINT person_id FK "NOT NULL"
        BIGINT affiliation_role_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(person_id, affiliation_role_id)"
    }

    student {
        BIGINT student_id PK
        BIGINT affiliation_id FK "NOT NULL"
        VARCHAR email_internal "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(affiliation_id, email_internal)"
    }

    employment_category {
        BIGINT employment_category_id PK
        VARCHAR name "NOT NULL"
        _ UNIQUE "(name)"
    }

    employment {
        BIGINT employment_id PK
        BIGINT affiliation_id FK "NOT NULL"
        BIGINT employment_category_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(affiliation_id, employment_category_id, date_start)"
    }

    consultant {
        BIGINT consultant_id PK
        BIGINT employment_id FK "NOT NULL"
        VARCHAR org_name
        VARCHAR org_number
        BOOLEAN f_skatt
        NUMERIC rate_hourly
        TEXT address
    }

    full_time {
        BIGINT full_time_id PK
        BIGINT employment_id FK "NOT NULL"
        NUMERIC salary_monthly
        SMALLINT hours_weekly
    }

    teacher {
        BIGINT teacher_id PK
        BIGINT employment_id FK "NOT NULL"
        _ UNIQUE "(employment_id)"
    }

    manager {
        BIGINT manager_id PK
        BIGINT employment_id FK "NOT NULL"
        _ UNIQUE "(employment_id)"
    }

    branch {
        BIGINT branch_id PK
        VARCHAR name "NOT NULL"
        VARCHAR city "NOT NULL"
        VARCHAR address
        _ UNIQUE "(name, city)"
    }

    program {
        BIGINT program_id PK
        VARCHAR name "NOT NULL"
        VARCHAR code "NOT NULL"
        SMALLINT cycle "NOT NULL, CHECK(1-3)"
        TEXT description
        _ UNIQUE "(code, cycle)"
    }

    program_branch {
        BIGINT program_branch_id PK
        BIGINT program_id FK "NOT NULL"
        BIGINT branch_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(program_id, branch_id, date_start)"
    }

    module_type {
        BIGINT module_type_id PK
        VARCHAR name "NOT NULL"
        _ UNIQUE "(name)"
    }

    module {
        BIGINT module_id PK
        BIGINT module_type_id FK "NOT NULL"
        BIGINT branch_id FK "NOT NULL"
        VARCHAR name "NOT NULL"
        VARCHAR code "NOT NULL"
        TEXT description
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(branch_id, code, date_start)"
    }

    module_program {
        BIGINT module_program_id PK
        BIGINT module_id FK "NOT NULL"
        BIGINT program_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(module_id, program_id, date_start)"
    }

    course {
        BIGINT course_id PK
        BIGINT program_id FK "NOT NULL"
        VARCHAR name "NOT NULL"
        VARCHAR code "NOT NULL"
        SMALLINT credits "NOT NULL"
        TEXT description
        _ UNIQUE "(program_id, code)"
    }

    course_module {
        BIGINT course_module_id PK
        BIGINT course_id FK "NOT NULL"
        BIGINT module_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(course_id, module_id, date_start)"
    }

    teacher_course {
        BIGINT teacher_course_id PK
        BIGINT teacher_id FK "NOT NULL"
        BIGINT course_module_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(teacher_id, course_module_id, date_start)"
    }

    student_course {
        BIGINT student_course_id PK
        BIGINT student_id FK "NOT NULL"
        BIGINT course_module_id FK "NOT NULL"
        VARCHAR grade_code FK
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(student_id, course_module_id, date_start)"
    }

    grade_type {
      VARCHAR grade_code PK
      BOOLEAN passed "NOT NULL"
    }

    cohort {
        BIGINT cohort_id PK
        BIGINT program_id FK "NOT NULL"
        BIGINT branch_id FK "NOT NULL"
        VARCHAR name "NOT NULL"
        VARCHAR code "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(program_id, code, date_start)"
    }

    student_cohort {
        BIGINT student_cohort_id PK
        BIGINT student_id FK "NOT NULL"
        BIGINT cohort_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(student_id, cohort_id, date_start)"
    }

    cohort_manager {
        BIGINT cohort_manager_id PK
        BIGINT cohort_id FK "NOT NULL"
        BIGINT manager_id FK "NOT NULL"
        DATE date_start "NOT NULL"
        DATE date_end
        _ UNIQUE "(cohort_id, manager_id, date_start)"
    }
```