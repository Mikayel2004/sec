from main import create_app, initialize_database

if __name__ == "__main__":
    print("Initializing database and generating data...")
    initialize_database()  # Handles both database setup and data generation

    print("Starting Flask server...")
    app = create_app()
    app.run(debug=True)
