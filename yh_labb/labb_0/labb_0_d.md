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

---
