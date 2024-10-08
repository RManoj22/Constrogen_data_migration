import config
from utils.logger import logger
from services.loaders.load_bills import load_bills
from services.loaders.load_items import load_items
from services.loaders.load_vendors import load_vendors
from services.loaders.load_projects import load_projects
from database.db_connection import get_db_connection

if __name__ == "__main__":
    logger.info("Starting the application")

    conn = get_db_connection()
    if conn:
        try:
            logger.info("Successfully connected to the database")
            conn.autocommit = False

            counters = {}

            if config.LOAD_PROJECTS:
                counters["projects"] = load_projects(conn)

            if config.LOAD_ITEMS:
                counters["items"] = load_items(conn)

            if config.LOAD_VENDORS:
                counters["vendors"] = load_vendors(conn)

            if config.LOAD_BILLS:
                counters["purchase order"] = load_bills(conn)

            logger.info(f"Counters: {counters}")

        except Exception as e:
            conn.rollback()
            logger.error(f"An error occurred during operations: {e}")
            raise

        finally:
            conn.close()
            logger.info("Database connection closed")
