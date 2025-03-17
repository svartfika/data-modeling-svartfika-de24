# exercise_1

## exercise_1_0

> Going back to the hospital exercise from exercise0, task 1, we will build logical and physical data models. This is the conceptual data model after we've added the composite entities to take care of many-to-many relationships.

```mermaid
erDiagram
    Hospital ||--|{ HospitalDepartment : ""
    Department ||--|{ HospitalDepartment : ""

    Hospital ||--|{ HospitalDoctor : ""
    Department ||--|{ DepartmentDoctor : ""

    Doctor ||--|{ DepartmentDoctor : ""
    Doctor ||--|{ HospitalDoctor : ""
```

### exercise_0_0_a

a) Create a logical data model using lucidcharts

```mermaid
erDiagram
    Hospital ||--|{ HospitalDepartment : ""
    Department ||--|{ HospitalDepartment : ""

    Hospital ||--|{ HospitalDoctor : ""
    Department ||--|{ DepartmentDoctor : ""

    Doctor ||--|{ DepartmentDoctor : ""
    Doctor ||--|{ HospitalDoctor : ""

    Hospital {
        _ Hospital_ID
        _ Hospital_Name
        _ Hospital_Address
    }

    Department {
        _ Department_ID
        _ Department_Name
    }

    HospitalDepartment {
        _ Hospital_ID
        _ Department_ID
    }

    Doctor {
        _ Docotor_ID
        _ Doctor_Name
    }

    HospitalDoctor {
        _ Hospital_ID
        _ Doctor_ID
    }

    DepartmentDoctor {
        _ Department_ID
        _ Doctor_ID
    }

```

### exercise_0_0_b

b) Identify different keys on the various entities

```mermaid
erDiagram
    Hospital ||--|{ HospitalDepartment : ""
    Department ||--|{ HospitalDepartment : ""

    Hospital ||--|{ HospitalDoctor : ""
    Department ||--|{ DepartmentDoctor : ""

    Doctor ||--|{ DepartmentDoctor : ""
    Doctor ||--|{ HospitalDoctor : ""

    Hospital {
        _ Hospital_ID PK
        _ Hospital_Name
        _ Hospital_Address
    }

    Department {
        _ Department_ID PK
        _ Department_Name
    }

    HospitalDepartment {
        _ Hospital_ID FK
        _ Department_ID FK
    }

    Doctor {
        _ Docotor_ID PK
        _ Doctor_Name
    }

    HospitalDoctor {
        _ Hospital_ID FK
        _ Doctor_ID FK
    }

    DepartmentDoctor {
        _ Department_ID FK
        _ Doctor_ID FK
    }

```

### exercise_0_0_c

c) Identify child entities and parent entities. What makes them into parent/child relationships?

...

### exercise_0_0_d

d) Create a physical data model using dbdiagram

> See `exercise_1_0.dmbl` ...

### exercise_0_0_e

e) Create a few tables manually, insert given data plus some more, and try to manually link foreign keys to primary keys.  
Can you satisfy that a doctor can work at *several departments* **and** *several hospitals*?

```sql
CREATE TABLE hospital_doctor (
    hospital_id INTEGER references hospital
    doctor_id INTEGER references doctor
    PRIMARY KEY (hospital_id, doctor_id) -- UNIQUE and NOT NULL
)
```


> See `exercise_1_0.sql ...