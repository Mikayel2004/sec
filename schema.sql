-- schema.sql

-- Create the professor table
CREATE TABLE IF NOT EXISTS professor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    degree VARCHAR(50),
    department VARCHAR(50),
    position VARCHAR(50),
    info JSONB
);


-- Create the subject table
CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hours INTEGER NOT NULL,
    professor_id INTEGER REFERENCES professor(id) ON DELETE SET NULL
);

-- Create the schedule table
CREATE TABLE IF NOT EXISTS schedule (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subject(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    time TIME NOT NULL,
    group_name VARCHAR(50) NOT NULL
);

-- Add a JSONB field to the professor table
ALTER TABLE professor ADD COLUMN IF NOT EXISTS info JSONB;


-- Enable pg_trgm extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create a GIN index on the info column
CREATE INDEX IF NOT EXISTS idx_metadata_trgm
ON professor USING gin (info jsonb_path_ops);
