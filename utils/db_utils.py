import psycopg2
from psycopg2.extras import RealDictCursor
from config import config

def get_db_connection():
    params = config()
    return psycopg2.connect(
        host=params["host"],
        port=params["port"],
        user=params["db_owner"],
        password=params["admin_password"],
        dbname=params["db_name"],
        cursor_factory=RealDictCursor
    )
