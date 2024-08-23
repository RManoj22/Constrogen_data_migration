import os
import psycopg2
from dotenv import load_dotenv
from utils.logger import logger

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pwd = os.getenv("DB_PWD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
schema = os.getenv("DB_SCHEMA")

db_params = {
    'dbname': db_name,
    'user': db_user,
    'password': db_pwd,
    'host': db_host,
    'port': db_port,
    'options': f'-c search_path={schema}'
}


def get_db_connection():
    try:
        conn = psycopg2.connect(**db_params)
        logger.info("Connected to the database successfully")
        return conn
    except Exception as e:
        logger.error(f"Unable to connect to the database: {e}")
        return None
