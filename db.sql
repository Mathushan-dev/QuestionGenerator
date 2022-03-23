CREATE TABLE IF NOT EXISTS public.questions
(
    "questionId" text COLLATE pg_catalog."default" NOT NULL,
    context text COLLATE pg_catalog."default",
    question text COLLATE pg_catalog."default",
    answer text COLLATE pg_catalog."default",
    options text COLLATE pg_catalog."default",
    "questionNumber" text COLLATE pg_catalog."default",
    "questionSetCode" text COLLATE pg_catalog."default",
    CONSTRAINT questions_pkey PRIMARY KEY ("questionId")
)

TABLESPACE pg_default;

CREATE TABLE IF NOT EXISTS public.users
(
    "userId" text COLLATE pg_catalog."default" NOT NULL,
    "fName" text COLLATE pg_catalog."default" NOT NULL,
    "lName" text COLLATE pg_catalog."default" NOT NULL,
    "hashedPassword" text COLLATE pg_catalog."default" NOT NULL,
    "attemptedQuestionIds" text COLLATE pg_catalog."default",
    "questionScores" text COLLATE pg_catalog."default",
    "numberOfAttempts" text COLLATE pg_catalog."default",
    "attemptedDates" text COLLATE pg_catalog."default",
    "attemptedTimes" text COLLATE pg_catalog."default",
    CONSTRAINT users_pkey PRIMARY KEY ("userId")
)

TABLESPACE pg_default;