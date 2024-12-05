from main import create_app, initialize_database

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    print("Starting Flask server...")

    app = create_app()  # Call create_app to initialize the app
    app.run(debug=True)  # Start the server

