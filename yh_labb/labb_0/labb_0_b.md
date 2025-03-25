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
    PERSON
    EMPLOYEE
    TEACHER
    MANAGER

    PERSON }o--o{ EMPLOYEE : "is employed"
    EMPLOYEE }o--o{ TEACHER : "has role"
    EMPLOYEE }o--o{ MANAGER : "has role"
```

#### Person to student role

```mermaid
erDiagram
    PERSON
    STUDENT

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
    PERSON ||--o{ AFFILIATION : ""
    AFFILIATION ||--o| EMPLOYEE : "is affiliated as"
    AFFILIATION ||--o| STUDENT : "is affiliated as"

    EMPLOYEE }o--o{ TEACHER : "may have the role"
    EMPLOYEE }o--o{ MANAGER : "may have the role"

    EMPLOYEE ||--o| "CONSULTANT" : "may be"
    EMPLOYEE ||--o| "FULL-TIME" : "may be"
```