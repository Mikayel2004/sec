from flask import Flask
from routes import register_routes
from db.DBInit import initDb
from config import config
from db.DataGen import  generate_data
def initialize_database():
    """Initialize the database using parameters from the config."""
    db_params = config()
    initDb(
        host=db_params["host"],
        port=db_params["port"],
        admin_user=db_params["admin_user"],
        admin_password=db_params["admin_password"],
        db_name=db_params["db_name"]
    )

def DataGen():
    generate_data()

def create_app():
    app = Flask(__name__)
    print("Registering routes...")
    register_routes(app)
    return app

