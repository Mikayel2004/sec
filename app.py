from main import create_app, initialize_database

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    print("Starting Flask server...")

    app = create_app()  # Correctly calling create_app without arguments
    app.run(debug=True)  # Start the server
