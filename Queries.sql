-- Sample Queries for CISD Data Warehouse

-- 1. List all students with gender and attendance
SELECT student_id, gender, attendance
FROM public.student_profile;

-- 2. List all exam scores for students
SELECT student_id, exam_score
FROM public.student_academics;

-- 3. Find the average exam score by household income bracket
SELECT *
FROM "DM_acadamic review".avg_exam_score_by_income;

-- 4. List all students flagged as "At Risk"
SELECT *
FROM "DM_acadamic review".at_risk_students;

-- 5. Count of "At Risk" students
SELECT COUNT(*) AS at_risk_count
FROM "DM_acadamic review".at_risk_students
WHERE risk_status = 'At Risk';

-- 6. Show risk score for each student
SELECT *
FROM "DM_acadamic review".student_risk_vw;

-- 7. For a given student, see their academic review details
SELECT *
FROM "DM_acadamic review".academic_review_vw
WHERE student_id = 101;  -- replace with any student_id

-- 8. Get average attendance by gender
SELECT gender, AVG(attendance) AS avg_attendance
FROM public.student_profile
GROUP BY gender
ORDER BY avg_attendance DESC;

-- 9. Which income bracket has the most students?
SELECT family_income, COUNT(*) AS num_students
FROM public.household_profile
GROUP BY family_income
ORDER BY num_students DESC;