#/db/DBIinit.py

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import config

def initDb(host, port, admin_user, admin_password, db_name):
    # Connect to the admin database (default: "postgres")
    try:
        admin_conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            dbname="postgres"  # Admin typically connects to the default 'postgres' database
        )
        admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Enable autocommit mode
        print(f"Connected to the admin database on {host}:{port}")
        
        with admin_conn.cursor() as admin_cursor:
            # Check if the database exists
            print(f"Checking if the database '{db_name}' exists...")
            admin_cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s;",
                (db_name,)  # Correct tuple formatting
            )
            if not admin_cursor.fetchone():
                print(f"Database '{db_name}' does not exist. Creating it now...")
                create_db_query = sql.SQL("CREATE DATABASE {db} OWNER {owner}").format(
                    db=sql.Identifier(db_name),
                    owner=sql.Identifier(admin_user)
                )
                admin_cursor.execute(create_db_query)
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error during database initialization: {e}")
        raise
    finally:
        admin_conn.close()

    # Connect to the created database and initialize tables
    try:
        db_conn = psycopg2.connect(
            host=host,
            port=port,
            user=admin_user,
            password=admin_password,
            dbname=db_name
        )
        print(f"Connected to the database '{db_name}' to initialize tables...")
        with db_conn.cursor() as cursor:
            with open("schema.sql", "r") as schema_file:  # Path to SQL schema
                schema_sql = schema_file.read()
                cursor.execute(schema_sql)
                db_conn.commit()
                print("Tables initialized successfully.")
    except Exception as e:
        print(f"Error during table initialization: {e}")
        raise
    finally:
        db_conn.close()


