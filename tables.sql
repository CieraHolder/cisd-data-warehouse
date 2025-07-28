CREATE TABLE public.student_profile (
    student_id SERIAL PRIMARY KEY,
    gender VARCHAR(20),
    peer_influence VARCHAR(50),
    learning_disabilities BOOLEAN,
    distance_from_home NUMERIC(5,2),
    motivation_level VARCHAR(20),
    sleep_hours NUMERIC(3,1),
    attendance NUMERIC(5,2)
);

CREATE TABLE public.household_profile (
    household_id SERIAL PRIMARY KEY,
    parental_education_level VARCHAR(100),
    parental_involvement VARCHAR(100),
    internet_access BOOLEAN,
    family_income VARCHAR(50),
    distance_from_home NUMERIC(5,2),
    access_to_resources BOOLEAN
);
CREATE TABLE public.student_address (
    address_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES public.student_profile(student_id),
    street VARCHAR(1000),
    city VARCHAR(1000),
    state VARCHAR(1000),
    zipcode INT
);

CREATE TABLE public.student_academics (
    student_record_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES public.student_profile(student_id),
    hours_studied NUMERIC(4,1),
    previous_scores NUMERIC(5,2),
    tutoring_sessions INT,
    teacher_quality VARCHAR(50),
    school_type VARCHAR(50),
    attendance NUMERIC(5,2),
    exam_score NUMERIC(5,2)
);
CREATE TABLE public.dim_student (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    gender VARCHAR(20),
    dob DATE
);

CREATE TABLE public.dim_school (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(100),
    school_type VARCHAR(50),
    address VARCHAR(200)
);

CREATE TABLE public.dim_date (
    date_id SERIAL PRIMARY KEY,
    date DATE,
    year INT,
    semester VARCHAR(10)
);

CREATE TABLE public.dim_household (
    household_id SERIAL PRIMARY KEY,
    family_income VARCHAR(50),
    parental_education_level VARCHAR(100)
);
CREATE TABLE public.dim_school (
    school_id SERIAL PRIMARY KEY,
    school_name VARCHAR(100),
    school_type VARCHAR(50),
    address VARCHAR(200)
);
CREATE TABLE public.dim_date (
    date_id SERIAL PRIMARY KEY,
    date DATE,
    year INT,
    semester VARCHAR(10)
);
CREATE TABLE public.dim_household (
    household_id SERIAL PRIMARY KEY,
    family_income VARCHAR(50),
    parental_education_level VARCHAR(100)
);
CREATE TABLE public.dim_student (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100),
    gender VARCHAR(20),
    dob DATE
);
CREATE TABLE public.fact_academic_performance (
    fact_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES public.dim_student(student_id),
    school_id INT REFERENCES public.dim_school(school_id),
    date_id INT REFERENCES public.dim_date(date_id),
    household_id INT REFERENCES public.dim_household(household_id),
    exam_score NUMERIC(5,2),
    attendance NUMERIC(5,2)
    -- add more facts as needed
);