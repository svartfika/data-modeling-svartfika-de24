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
  CHAR code
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
  CHAR code
  TEXT description
  DATE date_start
  DATE date_end
}

COURSE {
  SERIAL course_id PK
  INTEGER module_id FK
  VARCHAR name
  CHAR code
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
