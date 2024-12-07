from main import create_app, initialize_database

if __name__ == "__main__":
    # Initialize the database
    print("Initializing database...")
    initialize_database()

    # Create and run the Flask app
    app = create_app()  # This ensures the app is defined
    print("Starting Flask server...")
    app.run(debug=True)  # `debug=True` for development; set `False` in production
