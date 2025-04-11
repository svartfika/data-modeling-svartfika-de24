SET search_path TO yh;


INSERT INTO yh.module (module_type_id, branch_id, name, code, date_start, date_end)
VALUES (
    (SELECT module_type_id FROM yh.module_type WHERE name = 'EXTRA'),
    (SELECT branch_id FROM yh.branch WHERE name = 'STI Liljeholmen'),
    'Extra - Curriculum Stockholm - HT24',
    'STO_EXTRA_HT24',
    '2024-08-18',
    '2025-12-22'
);

INSERT INTO yh.course (name, code, credits)
VALUES (
    'Storytelling',
    'STO_EXTRA_STORY',
    2
);

INSERT INTO yh.course_module (course_id, module_id, date_start, date_end)
VALUES (
    (SELECT course_id FROM yh.course WHERE code = 'STO_EXTRA_STORY'),
    (SELECT m.module_id
        FROM yh.module m
        JOIN yh.branch b ON m.branch_id = b.branch_id
        WHERE m.code = 'STO_EXTRA_HT24'
        AND m.date_start = '2024-08-18'
        AND b.name = 'STI Liljeholmen'),
    '2024-09-29',
    '2024-11-10'
);


-- List all courses not in a program
SELECT DISTINCT
    c.course_id,
    c.name AS course_name,
    c.code AS course_code,
    c.credits
FROM
    yh.course AS c
JOIN
    yh.course_module AS cm ON c.course_id = cm.course_id
JOIN
    yh.module AS m ON cm.module_id = m.module_id
JOIN
    yh.branch AS b ON m.branch_id = b.branch_id
WHERE
    b.name = 'STI Liljeholmen'
AND
    NOT EXISTS (
        SELECT 1
        FROM yh.program_course AS pc
        WHERE pc.course_id = c.course_id
    );