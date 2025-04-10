## Uppgift 0 - datamodellering

### 0_d

> Bygg nu en logisk modell baserat pá den konceptuella

#### Entities id relationships

- **BRANCH**
    - branch_id

- *ModuleType*
    - module_type_id
    - module_type_name
    - module_type_description
- **MODULE**
    - module_id
    - module_type_id
    - branch_id

- **PROGRAM**
    - program_id
- *ProgramBranch*
    - program_branch_id
    - program_id
    - branch_id
- *ModuleProgram*
    - module_program_id
    - module_id
    - program_id

- **COURSE**
    - course_id
    - module_id

- **PERSON**
    - person_id
- *AffiliationRole*
    - affiliation_role_id
    - affiliation_role_name
    - affiliation_role_description
- **AFFILIATION**
    - affiliation_id
    - person_id
    - affiliation_type_id

- **EMPLOYEE**
    - employee_id
    - affiliation_id
    - employee_type_id
- *EmployeeCategory*
    - employee_category_id
    - employee_category_name
    - employee_category_description
- **CONSULTANT**
    - employee_id
- **FULL-TIME**
    - employee_id

- **MANAGER**
    - manager_id
    - employee_id
- *ProgramManager*
    - program_manager_id
    - program_id
    - manager_id

- **TEACHER**
    - teacher_id
    - employee_id
- *CourseTeacher*
    - course_teacher_id
    - course_id
    - teacher_id

- **STUDENT**
    - student_id
    - affiliation_id
    - program_id
- *CourseStudent*
    - course_student_id
    - course_id
    - student_id

---

```mermaid
erDiagram
    PROGRAM ||--|{ ProgramBranch : "offered at"
    BRANCH  ||--|{ ProgramBranch : "offers"

    BRANCH  ||--|{ MODULE : "offers"
    MODULE  ||--|{ ModuleProgram : "part of"
    PROGRAM ||--|{ ModuleProgram : "includes"
    MODULE  ||--o{ COURSE : "contains"
    MODULE  ||--|| ModuleType : "has a"

    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"
    AffiliationRole ||--|{ AFFILIATION : "specifies"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"
    EMPLOYEE ||--|| EmployeeCategory : "belongs to"

    EMPLOYEE ||--o| MANAGER : "is"
    PROGRAM  ||--|{ ProgramManager : "is managed by"
    MANAGER  ||--|{ ProgramManager : "manages"

    EMPLOYEE ||--o| TEACHER : "is"
    COURSE   ||--|{ CourseTeacher : "is taught by"
    TEACHER  ||--|{ CourseTeacher : "teaches"

    PROGRAM ||--o{ STUDENT : "has enrolled"
    COURSE  ||--|{ CourseStudent : "has enrolled"
    STUDENT ||--|{ CourseStudent : "participate"
```

---

```mermaid
erDiagram
PROGRAM ||--|{ ProgramBranch : "offered at"
BRANCH  ||--|{ ProgramBranch : "offers"

BRANCH  ||--|{ MODULE : "offers"
MODULE  ||--|{ ModuleProgram : "part of"
PROGRAM ||--|{ ModuleProgram : "includes"
MODULE  ||--o{ COURSE : "contains"
MODULE  ||--|| ModuleType : "has a"

PERSON      ||--|| AFFILIATION : "has"
AFFILIATION ||--|{ EMPLOYEE : "role defined as"
AFFILIATION ||--|{ STUDENT : "role defined as"
AffiliationRole ||--|{ AFFILIATION : "specifies"

BRANCH   ||--o{ EMPLOYEE : "employs"
EMPLOYEE ||--o| CONSULTANT : "is classified as"
EMPLOYEE ||--o| FULL-TIME : "is classified as"
EMPLOYEE ||--|| EmployeeCategory : "belongs to"

EMPLOYEE ||--o| MANAGER : "is"
PROGRAM  ||--|{ ProgramManager : "is managed by"
MANAGER  ||--|{ ProgramManager : "manages"

EMPLOYEE ||--o| TEACHER : "is"
COURSE   ||--|{ CourseTeacher : "is taught by"
TEACHER  ||--|{ CourseTeacher : "teaches"

PROGRAM ||--o{ STUDENT : "has enrolled"
COURSE  ||--|{ CourseStudent : "has enrolled"
STUDENT ||--|{ CourseStudent : "participate"

BRANCH {
_ branch_id
}

ModuleType {
_ module_type_id
_ module_type_name
_ module_type_description
}

MODULE {
_ module_id
_ module_type_id
_ branch_id
}

PROGRAM {
_ program_id
}

ProgramBranch {
_ program_branch_id
_ program_id
_ branch_id
}

ModuleProgram {
_ module_program_id
_ module_id
_ program_id
}

COURSE {
_ course_id
_ module_id
}

PERSON {
_ person_id
}

AffiliationRole {
_ affiliation_role_id
_ affiliation_role_name
_ affiliation_role_description
}

AFFILIATION {
_ affiliation_id
_ person_id
}

EMPLOYEE {
_ employee_id
_ affiliation_id
}

EmployeeCategory {
_ employee_category_id
_ employee_category_name
_ employee_category_description
}

CONSULTANT {
_ employee_id
}

FULL-TIME {
_ employee_id
}

MANAGER {
_ manager_id
_ employee_id
}

ProgramManager {
_ program_manager_id
_ program_id
_ manager_id
}

TEACHER {
_ teacher_id
_ employee_id
}

CourseTeacher {
_ course_teacher_id
_ course_id
_ teacher_id
}

STUDENT {
_ student_id
_ affiliation_id
_ program_id
}

CourseStudent {
_ course_student_id
_ course_id
_ student_id
}


```

#### Added additional fields

```mermaid
erDiagram
PROGRAM ||--|{ ProgramBranch : "offered at"
BRANCH  ||--|{ ProgramBranch : "offers"

BRANCH  ||--|{ MODULE : "offers"
MODULE  ||--|{ ModuleProgram : "part of"
PROGRAM ||--|{ ModuleProgram : "includes"
MODULE  ||--o{ COURSE : "contains"
MODULE  ||--|| ModuleType : "has a"

PERSON      ||--|| AFFILIATION : "has"
AFFILIATION ||--|{ EMPLOYEE : "role defined as"
AFFILIATION ||--|{ STUDENT : "role defined as"
AffiliationRole ||--|{ AFFILIATION : "specifies"

BRANCH   ||--o{ EMPLOYEE : "employs"
EMPLOYEE ||--o| CONSULTANT : "is classified as"
EMPLOYEE ||--o| FULL-TIME : "is classified as"
EMPLOYEE ||--|| EmployeeCategory : "belongs to"

EMPLOYEE ||--o| MANAGER : "is"
PROGRAM  ||--|{ ProgramManager : "is managed by"
MANAGER  ||--|{ ProgramManager : "manages"

EMPLOYEE ||--o| TEACHER : "is"
COURSE   ||--|{ CourseTeacher : "is taught by"
TEACHER  ||--|{ CourseTeacher : "teaches"

PROGRAM ||--o{ STUDENT : "has enrolled"
COURSE  ||--|{ CourseStudent : "has enrolled"
STUDENT ||--|{ CourseStudent : "participate"

BRANCH {
_ branch_id

_ name
_ city
_ address
}

ModuleType {
_ module_type_id

_ name
_ description
}

MODULE {
_ module_id
_ module_type_id
_ branch_id

_ name
_ date_start
_ date_end
}

PROGRAM {
_ program_id

_ name
_ date_start
_ date_end
_ cycle
}

ProgramBranch {
_ program_branch_id
_ program_id
_ branch_id
}

ModuleProgram {
_ module_program_id
_ module_id
_ program_id
}

COURSE {
_ course_id
_ module_id

_ name
_ code
_ credits
_ date_start
_ date_end
}

PERSON {
_ person_id

_ last_name
_ first_name
_ identity_number
_ address
_ phone
_ email_private
}

AffiliationRole {
_ affiliation_role_id

_ name
_ description
}

AFFILIATION {
_ affiliation_id
_ person_id
_ affiliation_role_id
}

EMPLOYEE {
_ employee_id
_ affiliation_id

_ date_start
_ date_end
}

EmployeeCategory {
_ employee_category_id

_ name
_ description
}

CONSULTANT {
_ employee_id
_ org_name
_ org_number
_ f_skatt
_ address
_ rate
}

FULL-TIME {
_ employee_id

_ salary
_ hours_weekly
}

MANAGER {
_ manager_id
_ employee_id
}

ProgramManager {
_ program_manager_id
_ program_id
_ manager_id
}

TEACHER {
_ teacher_id
_ employee_id
}

CourseTeacher {
_ course_teacher_id
_ course_id
_ teacher_id
}

STUDENT {
_ student_id
_ affiliation_id
_ program_id

_ email_internal
}

CourseStudent {
_ course_student_id
_ course_id
_ student_id
}


```

---

#### TODO 
Found a big error: Managers *do not* manage programs, they **manage student cohorts**!

---

#### Cohorts, students and managers

- MANAGER
- STUDENT
- COHORT
- StudentCohort
- ManagerCohort

Logical:

```mermaid
erDiagram
STUDENT ||--|{ StudentCohort : "belongs to"
COHORT  ||--|{ StudentCohort : "contains"
MANAGER ||--|{ ManagerCohort : "manages"
COHORT  ||--|{ ManagerCohort : "is managed by"
```

Conceptual:

```mermaid
erDiagram
STUDENT }|--|{ COHORT : "belongs to"
MANAGER }|--|{ COHORT : "manages"
```

#### Adding cohorts to main diagram

```mermaid
erDiagram
PROGRAM ||--|{ ProgramBranch : "offered at"
BRANCH  ||--|{ ProgramBranch : "offers"

BRANCH  ||--|{ MODULE : "offers"
MODULE  ||--|{ ModuleProgram : "part of"
PROGRAM ||--|{ ModuleProgram : "includes"
MODULE  ||--o{ COURSE : "contains"
MODULE  ||--|| ModuleType : "has a"

PERSON      ||--|| AFFILIATION : "has"
AFFILIATION ||--|{ EMPLOYEE : "role defined as"
AFFILIATION ||--|{ STUDENT : "role defined as"
AffiliationRole ||--|{ AFFILIATION : "specifies"

BRANCH   ||--o{ EMPLOYEE : "employs"
EMPLOYEE ||--o| CONSULTANT : "is classified as"
EMPLOYEE ||--o| FULL-TIME : "is classified as"
EMPLOYEE ||--|| EmployeeCategory : "belongs to"

EMPLOYEE ||--o| MANAGER : "is"
PROGRAM  ||--|{ ProgramManager : "is managed by"
MANAGER  ||--|{ ProgramManager : "manages"
MANAGER  ||--|{ ManagerCohort : "manages"
COHORT   ||--|{ ManagerCohort : "is managed by"

EMPLOYEE ||--o| TEACHER : "is"
COURSE   ||--|{ CourseTeacher : "is taught by"
TEACHER  ||--|{ CourseTeacher : "teaches"

PROGRAM ||--o{ STUDENT : "has enrolled"
COURSE  ||--|{ CourseStudent : "has enrolled"
STUDENT ||--|{ CourseStudent : "participate"
STUDENT ||--|{ StudentCohort : "belongs to"
COHORT  ||--|{ StudentCohort : "contains"

```

Sorted for elk render:

```mermaid
erDiagram
BRANCH  ||--o{ EMPLOYEE : ""
BRANCH  ||--|{ MODULE : ""

PROGRAM ||--|{ ProgramBranch : ""
BRANCH  ||--|{ ProgramBranch : ""

MODULE  ||--|{ ModuleProgram : ""
PROGRAM ||--|{ ModuleProgram : ""

MODULE  ||--|| ModuleType : ""
MODULE  ||--o{ COURSE : ""

MANAGER ||--|{ ManagerCohort : ""
COHORT  ||--|{ ManagerCohort : ""

PROGRAM ||--o{ STUDENT : ""

EMPLOYEE ||--o| TEACHER : ""
EMPLOYEE ||--o| MANAGER : ""

STUDENT ||--|{ StudentCohort : ""
COHORT  ||--|{ StudentCohort : ""

COURSE  ||--|{ CourseTeacher : ""
TEACHER ||--|{ CourseTeacher : ""

COURSE  ||--|{ CourseStudent : ""
STUDENT ||--|{ CourseStudent : ""

AffiliationRole ||--|{ AFFILIATION : ""
PERSON      ||--|| AFFILIATION : ""
AFFILIATION ||--|{ EMPLOYEE : ""
AFFILIATION ||--|{ STUDENT : ""

EMPLOYEE ||--o| FULL-TIME : ""
EMPLOYEE ||--|| EmployeeCategory : ""
EMPLOYEE ||--o| CONSULTANT : ""

```

```mermaid
erDiagram
BRANCH  ||--o{ EMPLOYEE : ""
BRANCH  ||--|{ MODULE : ""

PROGRAM ||--|{ ProgramBranch : ""
BRANCH  ||--|{ ProgramBranch : ""

MODULE  ||--|{ ModuleProgram : ""
PROGRAM ||--|{ ModuleProgram : ""

MODULE  ||--|| ModuleType : ""
MODULE  ||--o{ COURSE : ""

MANAGER ||--|{ CohortManager : ""
COHORT  ||--|{ CohortManager : ""

PROGRAM ||--o{ STUDENT : ""

EMPLOYEE ||--o| TEACHER : ""
EMPLOYEE ||--o| MANAGER : ""

STUDENT ||--|{ StudentCohort : ""
COHORT  ||--|{ StudentCohort : ""

COURSE  ||--|{ CourseTeacher : ""
TEACHER ||--|{ CourseTeacher : ""

COURSE  ||--|{ CourseStudent : ""
STUDENT ||--|{ CourseStudent : ""

AffiliationRole ||--|{ AFFILIATION : ""
PERSON      ||--|| AFFILIATION : ""
AFFILIATION ||--|{ EMPLOYEE : ""
AFFILIATION ||--|{ STUDENT : ""

EMPLOYEE ||--o| FULL-TIME : ""
EMPLOYEE ||--|| EmployeeCategory : ""
EMPLOYEE ||--o| CONSULTANT : ""

BRANCH {
_ branch_id

_ name
_ city
_ address
}

ModuleType {
_ module_type_id

_ name
_ description
}

MODULE {
_ module_id
_ module_type_id
_ branch_id

_ name
_ date_start
_ date_end
}

PROGRAM {
_ program_id

_ name
_ date_start
_ date_end
_ cycle
}

ProgramBranch {
_ program_branch_id
_ program_id
_ branch_id
}

ModuleProgram {
_ module_program_id
_ module_id
_ program_id
}

COURSE {
_ course_id
_ module_id

_ name
_ code
_ credits
_ date_start
_ date_end
}

PERSON {
_ person_id

_ last_name
_ first_name
_ identity_number
_ address
_ phone
_ email_private
}

AffiliationRole {
_ affiliation_role_id

_ name
_ description
}

AFFILIATION {
_ affiliation_id
_ person_id
_ affiliation_role_id
}

EMPLOYEE {
_ employee_id
_ affiliation_id

_ date_start
_ date_end
}

EmployeeCategory {
_ employee_category_id

_ name
_ description
}

CONSULTANT {
_ employee_id
_ org_name
_ org_number
_ f_skatt
_ address
_ rate
}

FULL-TIME {
_ employee_id

_ salary
_ hours_weekly
}

MANAGER {
_ manager_id
_ employee_id
}

COHORT {
_ cohort_id
}

CohortManager {
_ cohort_manager_id
_ cohort_id
_ manager_id
}

TEACHER {
_ teacher_id
_ employee_id
}

CourseTeacher {
_ course_teacher_id
_ course_id
_ teacher_id
}

STUDENT {
_ student_id
_ affiliation_id
_ program_id

_ email_internal
}

StudentCohort {
_ cohort_student_id
_ cohort_id
_ student_id
}

CourseStudent {
_ course_student_id
_ course_id
_ student_id
}
```

---

#### Re-ordering

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
  _ person_id
  _ last_name
  _ first_name
  _ identity_number
  _ address
  _ phone
  _ email_private
}

AffiliationRole {
  _ affiliation_role_id
  _ name
  _ description
}

AFFILIATION {
  _ affiliation_id
  _ person_id
  _ affiliation_role_id
}

EmployeeCategory {
  _ employee_category_id
  _ name
  _ description
}

EMPLOYEE {
  _ employee_id
  _ affiliation_id
  _ employee_category_id
  _ branch_id
  _ date_start
  _ date_end
}

STUDENT {
  _ student_id
  _ affiliation_id
  _ program_id
  _ email_internal
}

PROGRAM {
  _ program_id
  _ name
  _ date_start
  _ date_end
  _ cycle
}

BRANCH {
  _ branch_id
  _ name
  _ city
  _ address
}

ModuleType {
  _ module_type_id
  _ name
  _ description
}

MODULE {
  _ module_id
  _ module_type_id
  _ branch_id
  _ name
  _ date_start
  _ date_end
}

COURSE {
  _ course_id
  _ module_id
  _ name
  _ code
  _ credits
  _ date_start
  _ date_end
}

CONSULTANT {
  _ employee_id
  _ org_name
  _ org_number
  _ f_skatt
  _ address
  _ rate
}

FULL_TIME {
  _ employee_id
  _ salary
  _ hours_weekly
}

TEACHER {
  _ teacher_id
  _ employee_id
}

MANAGER {
  _ manager_id
  _ employee_id
}

ProgramBranch {
  _ program_branch_id
  _ program_id
  _ branch_id
}

ModuleProgram {
  _ module_program_id
  _ module_id
  _ program_id
}

CourseTeacher {
  _ course_teacher_id
  _ course_id
  _ teacher_id
}

CourseStudent {
  _ course_student_id
  _ course_id
  _ student_id
}

COHORT {
  _ cohort_id
}

StudentCohort {
  _ cohort_student_id
  _ cohort_id
  _ student_id
}

CohortManager {
  _ cohort_manager_id
  _ cohort_id
  _ manager_id
}
```

---

#### Adding more fields

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
  _ person_id
  _ last_name
  _ first_name
  _ identity_number
  _ address
  _ phone
  _ email_private
}

AffiliationRole {
  _ affiliation_role_id
  _ name
  _ description
}

AFFILIATION {
  _ affiliation_id
  _ person_id
  _ affiliation_role_id
}

EmployeeCategory {
  _ employee_category_id
  _ name
  _ description
}

EMPLOYEE {
  _ employee_id
  _ affiliation_id
  _ employee_category_id
  _ branch_id
  _ date_start
  _ date_end
}

STUDENT {
  _ student_id
  _ affiliation_id
  _ program_id
  _ email_internal
}

PROGRAM {
  _ program_id
  _ name
  _ code
  _ cycle
  _ description
  _ date_start
  _ date_end
}

BRANCH {
  _ branch_id
  _ name
  _ city
  _ address
}

ModuleType {
  _ module_type_id
  _ name
  _ description
}

MODULE {
  _ module_id
  _ module_type_id
  _ branch_id
  _ name
  _ code
  _ description
  _ date_start
  _ date_end
}

COURSE {
  _ course_id
  _ module_id
  _ name
  _ code
  _ credits
  _ description
  _ date_start
  _ date_end
}

CONSULTANT {
  _ employee_id
  _ org_name
  _ org_number
  _ f_skatt
  _ address
  _ rate
}

FULL_TIME {
  _ employee_id
  _ salary
  _ hours_weekly
}

TEACHER {
  _ teacher_id
  _ employee_id
}

MANAGER {
  _ manager_id
  _ employee_id
}

ProgramBranch {
  _ program_branch_id
  _ program_id
  _ branch_id
}

ModuleProgram {
  _ module_program_id
  _ module_id
  _ program_id
}

CourseTeacher {
  _ course_teacher_id
  _ course_id
  _ teacher_id
}

CourseStudent {
  _ course_student_id
  _ course_id
  _ student_id
}

COHORT {
  _ cohort_id
}

StudentCohort {
  _ cohort_student_id
  _ cohort_id
  _ student_id
}

CohortManager {
  _ cohort_manager_id
  _ cohort_id
  _ manager_id
}
```

---

#### Updating to reflect changes in the physical model

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
        INTEGER person_id PK
        STRING last_name
        STRING first_name
        STRING identity_number
        STRING address
        STRING phone
        STRING email_private
    }

    affiliation_role {
        INTEGER affiliation_role_id PK
        STRING name
    }

    affiliation {
        INTEGER affiliation_id PK
        INTEGER person_id FK
        INTEGER affiliation_role_id FK
        DATE date_start
        DATE date_end
    }

    student {
        INTEGER student_id PK
        INTEGER affiliation_id FK
        STRING email_internal
        DATE date_start
        DATE date_end
    }

    employment_category {
        INTEGER employment_category_id PK
        STRING name
    }

    employment {
        INTEGER employment_id PK
        INTEGER affiliation_id FK
        INTEGER employment_category_id FK
        DATE date_start
        DATE date_end
    }

    consultant {
        INTEGER consultant_id PK
        INTEGER employment_id FK
        STRING org_name
        STRING org_number
        BOOLEAN f_skatt
        NUMERIC rate_hourly
        STRING address
    }

    full_time {
        INTEGER full_time_id PK
        INTEGER employment_id FK
        NUMERIC salary_monthly
        INTEGER hours_weekly
    }

    teacher {
        INTEGER teacher_id PK
        INTEGER employment_id FK
    }

    manager {
        INTEGER manager_id PK
        INTEGER employment_id FK
    }

    branch {
        INTEGER branch_id PK
        STRING name
        STRING city
        STRING address
    }

    program {
        INTEGER program_id PK
        STRING name
        STRING code
        INTEGER cycle "CHECK(1-3)"
        STRING description
    }

    program_branch {
        INTEGER program_branch_id PK
        INTEGER program_id FK
        INTEGER branch_id FK
        DATE date_start
        DATE date_end
    }

    module_type {
        INTEGER module_type_id PK
        STRING name
    }

    module {
        INTEGER module_id PK
        INTEGER module_type_id FK
        INTEGER branch_id FK
        STRING name
        STRING code
        STRING description
        DATE date_start
        DATE date_end
    }

    module_program {
        INTEGER module_program_id PK
        INTEGER module_id FK
        INTEGER program_id FK
        DATE date_start
        DATE date_end
    }

    course {
        INTEGER course_id PK
        INTEGER program_id FK
        STRING name
        STRING code
        INTEGER credits
        STRING description
    }

    course_module {
        INTEGER course_module_id PK
        INTEGER course_id FK
        INTEGER module_id FK
        DATE date_start
        DATE date_end
    }

    teacher_course {
        INTEGER teacher_course_id PK
        INTEGER teacher_id FK
        INTEGER course_module_id FK
        DATE date_start
        DATE date_end
    }

    student_course {
        INTEGER student_course_id PK
        INTEGER student_id FK
        INTEGER course_module_id FK
        STRING grade_code FK
        DATE date_start
        DATE date_end
    }

    grade_type {
      STRING grade_code PK
      BOOLEAN passed
    }

    cohort {
        INTEGER cohort_id PK
        INTEGER program_id FK
        INTEGER branch_id FK
        STRING name
        STRING code
        DATE date_start
        DATE date_end
    }

    student_cohort {
        INTEGER student_cohort_id PK
        INTEGER student_id FK
        INTEGER cohort_id FK
        DATE date_start
        DATE date_end
    }

    cohort_manager {
        INTEGER cohort_manager_id PK
        INTEGER cohort_id FK
        INTEGER manager_id FK
        DATE date_start
        DATE date_end
    }
```