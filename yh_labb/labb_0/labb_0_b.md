## Uppgift 0 - datamodellering

### 0_b

> Gör en konceptuell modell baserat pa kravspecifikationen.

#### Entiteter

Entiterer utifrån beskriven kravspecifikation:

- studenter
    - förnamn
    - efternamn
    - personnummer
    - email
- utbildare
    - personuppgifter
    - anställningsform
        - konsult
        - fast anställd
- utbildningsledare
    - personuppgifter
    - ansvar för 3 klasser
- kurs
    - namn
    - kurskod
    - poäng
    - beskrivning
- program
    - anslutna kurser
    - beviljad omgång/klass
        - totalt/max 3
- fristående kurser
- anläggning
    - ort
- konsult-info
    - företagsnamn
    - organisationsnummer
    - "har F-skatt"
    - address
    - arvode/h
- fast anställd-info
    - personuppgifter
- känsliga uppgifter
    - personuppgifter
        - studenter
        - utbildare
        - utbildningsledare

---

Konceptuella entiteter:

- person-info
    - personuppgifter
        - förnamn
        - efternamn
        - personnummer
        - address
- anställnings-info
    - konsult
        - företag
        - organisationsnummer
        - f-skatt
        - arvode/h
    - fast
        - arbetstid/vecka
        - månadslön
- anställd
    - anläggning
    - person
    - roll
    - anställningsform
        - konsult
        - fast
- utbildningsledare
    - anställd person
    - kurser (<=3)
- utbildare
    - anställd person
    - kurser
- student
    - person
    - program
    - kurser
- program
    - omgång/klass (<=3)
    - kurser
    - start-datum
    - slut-datum
- kurs
    - utbildningsledare
    - utbildare
    - studenter
    - start-datum
    - slut-datum
- anläggning
    - anställda personer
    - program

### Diagram

#### Person to employment role

```mermaid
erDiagram
    PERSON }o--o{ EMPLOYEE : "is employed"
    EMPLOYEE }o--o{ TEACHER : "has role"
    EMPLOYEE }o--o{ MANAGER : "has role"
```

#### Person to student role

```mermaid
erDiagram
    PERSON }o--o{ STUDENT : "is a"
```

#### Combined

```mermaid
erDiagram
    PERSON }o--o{ EMPLOYEE : "is employed"
    EMPLOYEE }o--o{ TEACHER : "has role"
    EMPLOYEE }o--o{ MANAGER : "has role"
    PERSON }o--o{ STUDENT : "is enrolled"
```

#### With additional employment type

```mermaid
erDiagram
    PERSON }o--o{ EMPLOYEE : "may be employed"
    EMPLOYEE }o--o{ TEACHER : "may have the role"
    EMPLOYEE }o--o{ MANAGER : "may have the role"

    EMPLOYEE ||--o| "CONSULTANT" : "may be"
    EMPLOYEE ||--o| "FULL-TIME" : "may be"

    PERSON }o--o{ STUDENT : "may be enrolled"
```

#### With "role"

```mermaid
erDiagram
    PERSON ||--o{ ROLE : ""
    ROLE ||--o| EMPLOYEE : "is employed"
    ROLE ||--o| STUDENT : "is enrolled"
    EMPLOYEE }o--o{ TEACHER : "may have the role"
    EMPLOYEE }o--o{ MANAGER : "may have the role"
```

#### With "affiliation" and employment type

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"
```

---

#### Branch-level enteties

```mermaid
erDiagram
    BRANCH
    EMPLOYEE
    PROGRAM
    COURSE
```

#### Cardinality

```mermaid
erDiagram
    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--|{ PROGRAM : "manages"
    EMPLOYEE ||--o{ COURSE : "teaches"
```

> a branch offers *one or more programs*  
> a program is in *one branch* only  
> (a program *is not* in many branch locations)  
> branch to program  
> *one branch* to *one or more programs*  
> branch *one-to-zero/many* programs  

> *a program* contains *many courses*  
> a course is in exactly *one program*  
> one program *has many* courses  
> program *one-to-zero/many* courses  

> *a branch* employs *many employees*  
> *an employee* is employed to *exactly one branch*  
> *one branch* to *many employees*  
> branch *one-to-zero/many* employees  

> *an employee* can manage *zero or one programs*  
> *one program* can be managed my *one employee* 
> *one program* can not have *zero managers* 
> an employee *one-to-zero/one*  

> *one course* can be run by *one teacher/employee*  
> *one employee/teacher* can teach *many courses*  
> one employee *one-to-zero/many* courses  

#### Adding student

```mermaid
erDiagram
    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"
    PROGRAM  ||--o{ COURSE : "contains"
```
> *one student* can be in only *one program*
> *one prgoram* can have *many students*

```mermaid
erDiagram
    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"
    COURSE   }o--|| EMPLOYEE : "is taught by"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--|{ PROGRAM : "manages"
    EMPLOYEE ||--o{ COURSE : "teaches"
```

#### Adding teacher/manager
```mermaid
erDiagram
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"
```

```mermaid
erDiagram
    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"
```

#### Adding affiliation

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"
```

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"
```

#### Adding employment type

```mermaid
erDiagram
    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"
```

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"
```

---

#### Beta version

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"
```

```mermaid
erDiagram
    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    PROGRAM  ||--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"

    BRANCH   ||--o{ PROGRAM : "offers"
    PROGRAM  ||--o{ COURSE : "contains"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"
```

#### Adding course modules

```mermaid
erDiagram
    BRANCH  ||--|{ MODULE : "hosts"
    BRANCH  }o--o{ PROGRAM : "offers"
    PROGRAM ||--o{ MODULE : "includes"
    MODULE  ||--|{ COURSE : "contains"
```
> *one module* can be in only *one branch*  
> *one branch* can have *many modules*  
> *one branch* can have *zero or more programs*  

> *one program* can have *many modules*  
> *one module* can be in *only one program*  

> *one module* contains *one or many courses*  
> *one course* can be in *only one module*  

```mermaid
erDiagram
    BRANCH  ||--|{ MODULE : "hosts"
    BRANCH  }o--o{ PROGRAM : "offers"
    PROGRAM ||--o{ MODULE : "includes"
    MODULE  ||--|{ COURSE : "contains"

    PERSON      ||--|| AFFILIATION : "has"
    AFFILIATION ||--|{ EMPLOYEE : "role defined as"
    AFFILIATION ||--|{ STUDENT : "role defined as"

    BRANCH   ||--o{ EMPLOYEE : "employs"
    EMPLOYEE ||--o| TEACHER : "is"
    EMPLOYEE ||--o| MANAGER : "is"

    EMPLOYEE ||--o| CONSULTANT : "is classified as"
    EMPLOYEE ||--o| FULL-TIME : "is classified as"

    MANAGER  ||--|{ PROGRAM : "manages"
    TEACHER  ||--o{ COURSE : "teaches"

    PROGRAM  |o--o{ STUDENT : "has enrolled"
    STUDENT  }o--o{ COURSE : "participate in"
```