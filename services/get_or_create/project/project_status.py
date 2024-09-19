import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID
from queries.project.project_status import get_project_status, create_project_status

client_id = CLIENT_ID
company_id = COMPANY_ID


def get_or_create_project_status(conn, status_description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve project status with description: '{status_description}' and company ID: '{company_id}'")
            cursor.execute(get_project_status, (status_description, company_id))
            result = cursor.fetchone()

            if result:
                project_status_key = result[0]
                logger.info(
                    f"Project status '{status_description}' found with key: '{project_status_key}'")
                return project_status_key, False
            else:
                logger.info(
                    f"Project status '{status_description}' not found, creating new entry.")
                cursor.execute(create_project_status, (status_description, client_id, company_id))
                project_status_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new project status '{status_description}' with key: '{project_status_key}'")
                return project_status_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing project status '{status_description}': {e}")
        raise
