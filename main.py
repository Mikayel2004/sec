from flask import Flask
from routes import register_routes
from db.DBInit import initDb
from config import config

def initialize_database():
    """Initialize the database using parameters from the config."""
    print("Initializing database...")
    initDb(config())  # db_params should be a dictionary, not a function

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    register_routes(app)
    return app
