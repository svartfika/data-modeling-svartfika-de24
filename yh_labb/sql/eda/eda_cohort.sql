SET search_path TO yh ;


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


-- List all students enrolled in cohort with code 'DE24-Stockholm'
SELECT
    p.first_name,
    p.last_name,
    s.email_internal,
    c.name AS cohort_name
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
WHERE
    c.code = 'DE24-Stockholm'
ORDER BY
    p.last_name, p.first_name;


-- Count all courses the cohort with code 'DE24-Stockholm' is enrolled in
SELECT
    ch.code AS cohort_code,
    COUNT(cm.course_module_id) AS count_courses
FROM
    yh.cohort ch
JOIN
    yh.program_course pc ON ch.program_id = pc.program_id
JOIN
    yh.course_module cm ON pc.course_id = cm.course_id
JOIN
    yh.module m ON cm.module_id = m.module_id
WHERE
    ch.code = 'DE24-Stockholm'
    AND m.branch_id = ch.branch_id
GROUP BY
    ch.code;


-- List all affiliated teachers and managers for cohort with code 'DE24-Stockholm'
SELECT
    'MANAGER' AS role,
    p.first_name,
    p.last_name
FROM
    yh.person p
JOIN
    yh.affiliation a ON p.person_id = a.person_id
JOIN
    yh.employment e ON a.affiliation_id = e.affiliation_id
JOIN
    yh.manager m ON e.employment_id = m.employment_id
JOIN
    yh.cohort_manager cm ON m.manager_id = cm.manager_id
JOIN
    yh.cohort c ON cm.cohort_id = c.cohort_id
WHERE
    c.code = 'DE24-Stockholm'

UNION ALL

SELECT DISTINCT
    'TEACHER' AS role,
    p.first_name,
    p.last_name
FROM
    yh.person p
JOIN
    yh.affiliation a ON p.person_id = a.person_id
JOIN
    yh.employment e ON a.affiliation_id = e.affiliation_id
JOIN
    yh.teacher t ON e.employment_id = t.employment_id
JOIN
    yh.teacher_course tc ON t.teacher_id = tc.teacher_id
JOIN
    yh.course_module cm ON tc.course_module_id = cm.course_module_id
JOIN
    yh.module m ON cm.module_id = m.module_id
JOIN
    yh.course c ON cm.course_id = c.course_id
JOIN
    yh.program_course pc ON c.course_id = pc.course_id
JOIN
    yh.cohort target_cohort ON pc.program_id = target_cohort.program_id
    AND m.branch_id = target_cohort.branch_id
WHERE
    target_cohort.code = 'DE24-Stockholm'
ORDER BY
    role,
    last_name,
    first_name;