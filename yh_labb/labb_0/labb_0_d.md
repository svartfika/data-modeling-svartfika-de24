## Uppgift 0 - datamodellering

### 0_d

> Bygg nu en logisk modell baserat pá den konceptuella

#### Entities id relationships

- **BRANCH**
    - branch_id
- **PROGRAM**
    - program_id
    - branch_id
- **COURSE**
    - course_id
    - program_id

- **PERSON**
    - person_id
- *AffiliationType*
    - type_id
    - type_name
- **AFFILIATION**
    - affiliation_id
    - person_id
    - affiliation_type_id

- **EMPLOYEE**
    - employee_id
    - affiliation_id
    - employee_type_id
- *EmployeeType*
    - type_id
    - type_name
- **CONSULTANT**
    - employee_id
- **FULL-TIME**
    - employee_id

- **MANAGER**
    - manager_id
    - employee_id
- *ProgramManager*
    - program_id
    - manager_id

- **TEACHER**
    - teacher_id
    - employee_id
- *CourseTeacher*
    - course_id
    - teacher_id

- **STUDENT**
    - student_id
    - affiliation_id
    - program_id
- *CourseStudent*
    - course_id
    - student_id
