# utils/db_utils.py

import psycopg2
from config import config

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    db_params = config()
    connection = psycopg2.connect(
        host=db_params["host"],
        port=db_params["port"],
        user=db_params["admin_user"],
        password=db_params["admin_password"],
        dbname=db_params["db_name"]
    )
    return connection
