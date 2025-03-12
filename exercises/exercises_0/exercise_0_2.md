# exercise_0

## exercise_0_2

> A library called Bookly keeps track of books and members who borrow them. Each book has a title, author, and ISBN number. Each member has a membership ID, name, and contact information. A member can borrow multiple books, but each book can be borrowed by only one member at a time.

### exercise_0_2_a

a) Identify the **entities** and **attributes** for each entity.

> *Each book has a title, author, and ISBN number.*  
*Each member has a membership ID, name, and contact information.* 

- books
	- title
	- author
	- ISBN
- members
	- membership ID
	- name
	- contact information

### exercise_0_2_b

b) Determine the **relationship** between member and books.

> *A member can borrow multiple books,*  
*but each book can be borrowed by only one member at a time.*

single book loan, borrowing (verb), record of a loan

- member
    - *borrows* / is *borrowing*
    - "can borrow multiple books"
    - can appear in multiple loan records
- book
    - is *borrowed*
    - can only be borrowed by only one member at a time
    - can only appear in a single loan record

a member can borrow many books.  
a book can be borrowed by only one member.

```mermaid
erDiagram
    MEMBER ||--|{ BOOK : borrows
```

### exercise_0_2_c

c) Draw a **conceptual ERD** using crow foots notation.

> See `exercise_0_2.dmbl` ...
