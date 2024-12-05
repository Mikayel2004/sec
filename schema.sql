-- schema.sql
CREATE TABLE IF NOT EXISTS professor (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    degree VARCHAR(50),
    department VARCHAR(50),
    position VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    hours INTEGER NOT NULL,
    professor_id INTEGER REFERENCES professor(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS schedule (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subject(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    time TIME NOT NULL,
    group_name VARCHAR(50) NOT NULL
);
