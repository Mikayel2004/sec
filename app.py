from flask import render_template
from flask_migrate import Migrate

from main import create_app, initialize_database
from Models.models import db

if __name__ == "__main__":
    print("Initializing database and generating data...")
    initialize_database()  # This will initialize the DB and apply migrations

    print("Starting Flask server...")
    app = create_app()
    migrate = Migrate(app, db)
    app.run(debug=True)
