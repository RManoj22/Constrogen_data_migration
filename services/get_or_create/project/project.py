import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.project.project import get_project, create_project


client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_project(conn, description, status, units, address, state_key, city_key, project_type_key, project_code):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve project with description: '{description}'")
            cursor.execute(get_project, (description,))
            result = cursor.fetchone()

            if result:
                project_key = result[0]
                logger.info(
                    f"Project '{description}' found with key: '{project_key}'")
                return project_key, False
            else:
                logger.info(
                    f"Project '{description}' not found, creating new entry.")
                cursor.execute(create_project, (project_code, description, address, units, created_by,
                               created_at, city_key, client_id, company_id, status, project_type_key, state_key))
                project_key = cursor.fetchone()[0]
                logger.info(
                    f"Project '{description}' created with key: '{project_key}'")
                return project_key, True
    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing project '{description}': {e}")
        raise
