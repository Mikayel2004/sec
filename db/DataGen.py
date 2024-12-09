#/db/Datagen.py

from random import randint
from datetime import date, timedelta, datetime
from utils.faker_utils import fake

def generate_data(cursor):
    try:
        professors = [
            (fake.name(), fake.job(), fake.company_suffix(), fake.word())
            for _ in range(10)
        ]
        cursor.executemany("INSERT INTO professor (name, degree, department, position) VALUES (%s, %s, %s, %s);", professors)

        subjects = [
            (fake.bs(), randint(10, 40), randint(1, len(professors)))
            for _ in range(20)
        ]
        cursor.executemany("INSERT INTO subject (name, hours, professor_id) VALUES (%s, %s, %s);", subjects)

        schedules = [
            (randint(1, len(subjects)), date.today() + timedelta(days=randint(1, 30)), f"{randint(8, 18)}:00:00", fake.word().capitalize())
            for _ in range(50)
        ]
        cursor.executemany("INSERT INTO schedule (subject_id, date, time, group_name) VALUES (%s, %s, %s, %s);", schedules)
    except Exception as e:
        print(f"Error generating data: {e}")
