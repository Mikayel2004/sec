from flask import Flask

from Migrations.migrations import apply_migrations
from routes import register_routes
from db.DBInit import initDb
from config import config
from db.DataGen import generate_data
import psycopg2


def initialize_database():
    """Initialize the database and generate initial data using parameters from the config."""
    db_params = config()

    # Step 1: Initialize the database and tables
    initDb(
        host=db_params["host"],
        port=db_params["port"],
        admin_user=db_params["admin_user"],
        admin_password=db_params["admin_password"],
        db_name=db_params["db_name"]
    )

    # Step 2: Populate the database with initial data
    try:
        print("Generating initial data...")
        conn = psycopg2.connect(
            host=db_params["host"],
            port=db_params["port"],
            user=db_params["admin_user"],
            password=db_params["admin_password"],
            dbname=db_params["db_name"]
        )
        print("Connected to the database for data generation.")

        with conn.cursor() as cursor:
            generate_data(cursor)  # Generate data using the cursor
            conn.commit()  # Commit the changes
            print("Initial data generation completed successfully.")
    except Exception as e:
        print(f"Error during data generation: {e}")
        raise
    finally:
        conn.close()
    print("Applying migrations...")
    apply_migrations(db_params)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    print("Registering routes...")
    register_routes(app)
    return app
