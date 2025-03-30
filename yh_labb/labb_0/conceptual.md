---
    config:
        layout: elk
---
erDiagram
direction TB
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