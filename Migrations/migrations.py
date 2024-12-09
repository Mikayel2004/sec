# migrations.py

import psycopg2
from config import config

def apply_migrations(db_params):
    """Apply database migrations (adding columns and creating indexes)."""
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_params["host"],
            port=db_params["port"],
            user=db_params["admin_user"],
            password=db_params["admin_password"],
            dbname=db_params["db_name"]
        )
        print("Connected to the database for migrations.")

        with conn.cursor() as cursor:
            # Migration 1: Adding new columns
            print("Applying migration: Adding new columns...")
            cursor.execute("""
                ALTER TABLE professor ADD COLUMN IF NOT EXISTS email VARCHAR(255);
                ALTER TABLE subject ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)
            print("Columns added successfully.")

            # Migration 2: Creating indexes
            print("Applying migration: Creating indexes...")
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_professor_email ON professor(email);
                CREATE INDEX IF NOT EXISTS idx_subject_created_at ON subject(created_at);
            """)
            print("Indexes created successfully.")

            # Commit changes
            conn.commit()
            print("Migrations applied successfully.")
    except Exception as e:
        print(f"Error applying migrations: {e}")
        raise
    finally:
        conn.close()
