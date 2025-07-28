CREATE OR REPLACE VIEW "DM_acadamic review".academic_review_vw AS
SELECT
    sp.student_id,
    sp.gender,
    sp.motivation_level,
    sp.sleep_hours,
    sp.attendance AS student_attendance,
    sa.hours_studied,
    sa.previous_scores,
    sa.exam_score,
    sa.tutoring_sessions,
    sa.teacher_quality,
    sa.school_type,
    sa.attendance AS academic_attendance,
    hp.parental_education_level,
    hp.parental_involvement,
    hp.family_income,
    hp.internet_access
FROM public.student_profile sp
JOIN public.student_academics sa ON sp.student_id = sa.student_id
JOIN public.household_profile hp ON sp.student_id = hp.student_id;

CREATE OR REPLACE VIEW "DM_acadamic review".avg_exam_score_by_income AS
SELECT
    hp.family_income,
    ROUND(AVG(sa.exam_score), 2) AS avg_exam_score,
    COUNT(*) AS student_count
FROM public.student_academics sa
JOIN public.student_profile sp ON sa.student_id = sp.student_id
JOIN public.household_profile hp ON sp.student_id = hp.student_id
GROUP BY hp.family_income
ORDER BY hp.family_income;

CREATE OR REPLACE VIEW "DM_acadamic review".at_risk_students AS
SELECT
    sp.student_id,
    sp.gender,
    sa.exam_score,
    sa.attendance,
    CASE
        WHEN sa.exam_score < 70 OR sa.attendance < 80 THEN 'At Risk'
        ELSE 'On Track'
    END AS risk_status
FROM public.student_profile sp
JOIN public.student_academics sa ON sp.student_id = sa.student_id
WHERE sa.exam_score < 70 OR sa.attendance < 80;

CREATE OR REPLACE VIEW "DM_acadamic review".student_risk_vw AS
SELECT
    sp.student_id,
    sa.exam_score,
    sa.attendance,
    CASE
        WHEN sa.exam_score < 70 OR sa.attendance < 80 THEN 'At Risk'
        ELSE 'On Track'
    END AS risk_status,
    (CASE WHEN sa.exam_score < 70 THEN 1 ELSE 0 END +
     CASE WHEN sa.attendance < 80 THEN 1 ELSE 0 END) AS risk_score
FROM public.student_profile sp
JOIN public.student_academics sa ON sp.student_id = sa.student_id;