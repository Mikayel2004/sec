import psycopg2
from psycopg2 import sql
from config import config


def initDb(psycopg2, sql, host, port, admin_user, admin_password, db_name, db_owner):
    try:
        # Connect to the admin database
        with psycopg2.connect(
                host=host,
                port=port,
                admin_user=admin_user,
                admin_password=admin_password,
                db_name=db_name,
                db_owner=db_owner
        ) as admin_conn:
            print(f"Connected to the admin database on {host}:{port}")
            admin_conn.autocommit = True  # Required to run CREATE DATABASE
            with admin_conn.cursor() as admin_cursor:
                # Check if the database exists
                print(f"Checking if the database '{db_name}' exists...")
                admin_cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s;",
                    (db_name)
                )
                if not admin_cursor.fetchone():
                    print(f"Database '{db_name}' does not exist. Creating it now...")
                    admin_cursor.execute(
                        sql.SQL("CREATE DATABASE {dbname} OWNER {user}").format(
                            sql.Identifier(db_name),
                            sql.Identifier(admin_user)
                        )
                    )
                    print(f"Database '{db_name}' created successfully.")
                else:
                    print(f"Database '{db_name}' already exists.")

        # Connect to the created database and initialize tables
        print(f"Connecting to the database '{db_name}' to initialize tables...")
        with psycopg2.connect(
                host=host,
                port=port,
                admin_user=admin_user,
                admin_password=admin_password,
                db_name=db_name,
                db_owner=db_owner
        ) as db_conn:
            with db_conn.cursor() as cursor:
                with open("db/schema.sql", "r") as schema_file:  # Path to SQL schema
                    schema_sql = schema_file.read()
                    cursor.execute(schema_sql)
                    db_conn.commit()
                    print("Tables initialized successfully.")

    except Exception as e:
        print(f"Error during database initialization: {e}")
