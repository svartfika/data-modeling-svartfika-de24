SET search_path TO yh ;


-- Employment statistics
SELECT
    COUNT(DISTINCT p.person_id) AS total_employed,
    COUNT(DISTINCT p.person_id) FILTER (WHERE t.teacher_id IS NOT NULL) AS employed_teachers,
    COUNT(DISTINCT p.person_id) FILTER (WHERE m.manager_id IS NOT NULL) AS employed_managers,
    COUNT(DISTINCT p.person_id) FILTER (WHERE ec.name = 'CONSULTANT') AS employed_consultants,
    COUNT(DISTINCT p.person_id) FILTER (WHERE ec.name = 'FULL_TIME') AS employed_full_time,
    AVG(ft.salary_monthly) FILTER (WHERE ec.name = 'FULL_TIME') AS mean_monthly_salary_full_time,
    AVG(c.rate_hourly) FILTER (WHERE ec.name = 'CONSULTANT') AS mean_hourly_rate_consultant
FROM
    yh.person p
JOIN
    yh.affiliation a ON p.person_id = a.person_id
JOIN
    yh.employment e ON a.affiliation_id = e.affiliation_id
JOIN
    yh.employment_category ec ON e.employment_category_id = ec.employment_category_id
LEFT JOIN
    yh.teacher t ON e.employment_id = t.employment_id
LEFT JOIN
    yh.manager m ON e.employment_id = m.employment_id
LEFT JOIN
    yh.full_time ft ON e.employment_id = ft.employment_id
LEFT JOIN
    yh.consultant c ON e.employment_id = c.employment_id;