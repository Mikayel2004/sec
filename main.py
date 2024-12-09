from flask import Flask

from Migrations.migrations import apply_migrations
from Models.models import db
from routes import register_routes
from db.DBInit import initDb
from config import config
from db.DataGen import generate_data
import psycopg2
import os


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
    app = Flask(__name__, template_folder='template')

    # Load database configuration
    db_params = config()

    # Construct the SQLAlchemy database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_params['admin_user']}:{db_params['admin_password']}"
        f"@{db_params['host']}:{db_params['port']}/{db_params['db_name']}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    register_routes(app)
    return app

print("Current Working Directory:", os.getcwd())
