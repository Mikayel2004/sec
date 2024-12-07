from main import create_app, initialize_database
from db.DataGen import generate_data

if __name__ == "__main__":
    print("Initializing database...")
    initialize_database()
    print("Generating data...")
    generate_data()
    print("Starting Flask server...")

    app = create_app()  # Correctly calling create_app without arguments
    app.run(debug=True)  # Start the server
