SET search_path TO yh ;


-- List all programs
SELECT
    program_id, name, code, cycle
FROM 
    yh.program 
ORDER BY 
    name;


-- List all branches
SELECT 
    branch_id, name, city, address
FROM 
    yh.branch 
ORDER BY 
    city, name;


-- List all programs offered at branch 'STI Liljeholmen'
SELECT DISTINCT
    pr.name AS program_name,
    pr.code AS program_code,
    b.name AS branch_name,
    b.city AS branch_city
FROM 
    yh.program pr
JOIN 
    yh.program_branch pb ON pr.program_id = pb.program_id
JOIN 
    yh.branch b ON pb.branch_id = b.branch_id
WHERE 
    b.name = 'STI Liljeholmen'
    AND (pb.date_end IS NULL OR pb.date_end > CURRENT_DATE)
ORDER BY 
    pr.name;


-- List all branches and student count
SELECT
    b.name AS branch_name,
    b.city AS branch_city,
    COUNT(DISTINCT s.student_id) AS student_count
FROM
    yh.branch b
LEFT JOIN
    yh.cohort c ON b.branch_id = c.branch_id
LEFT JOIN
    yh.student_cohort sc ON c.cohort_id = sc.cohort_id
LEFT JOIN
    yh.student s ON sc.student_id = s.student_id
GROUP BY
    b.branch_id, b.city, b.name
ORDER BY
    b.city, b.name;


-- List all cohorts enrolled at branch 'STI Liljeholmen'
SELECT
    c.name AS cohort_name,
    c.code AS cohort_code,
    pr.name AS program_name,
    c.date_start AS cohort_start_date,
    c.date_end AS cohort_end_date,
    b.name AS branch_name
FROM
    yh.cohort c
JOIN
    yh.branch b ON c.branch_id = b.branch_id
JOIN
    yh.program pr ON c.program_id = pr.program_id
WHERE
    b.name = 'STI Liljeholmen'
    AND (c.date_end IS NULL OR c.date_end > CURRENT_DATE)
ORDER BY
    program_name, cohort_start_date, cohort_name;


-- List all students enrolled in the program 'Data Engineer' at branch 'STI Liljeholmen'
SELECT
    p.first_name,
    p.last_name,
    s.email_internal,
    c.name AS cohort_name,
    c.code AS cohort_code
FROM
    yh.person p
JOIN
    yh.affiliation a ON p.person_id = a.person_id
JOIN
    yh.student s ON a.affiliation_id = s.affiliation_id
JOIN
    yh.student_cohort sc ON s.student_id = sc.student_id
JOIN
    yh.cohort c ON sc.cohort_id = c.cohort_id
JOIN
    yh.program pr ON c.program_id = pr.program_id
JOIN
    yh.branch b ON c.branch_id = b.branch_id
WHERE
    pr.name = 'Data Engineer'
    AND b.name = 'STI Liljeholmen'
ORDER BY
    p.last_name, p.first_name;