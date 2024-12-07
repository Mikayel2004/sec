# app.py
from main import create_app, initialize_database

if __name__ == "__main__":
    print("Initializing database and generating data...")
    initialize_database()  # This will initialize the DB and apply migrations

    print("Starting Flask server...")
    app = create_app()
    app.run(debug=True)
