import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.project.project_type import get_project_type, create_project_type

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_project_type(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve project type: '{description}' with client id {client_id} and company id {company_id}")
            cursor.execute(get_project_type, (description, client_id, company_id))
            result = cursor.fetchone()

            if result:
                project_type_key = result[0]
                logger.info(
                    f"Project type '{description}' with client id {client_id} and company id {company_id} found with key: '{project_type_key}'")
                return project_type_key, False
            else:
                logger.info(
                    f"Project type '{description}' with client id {client_id} and company id {company_id} not found, creating new entry.")
                cursor.execute(create_project_type, (description,
                               created_by, created_at, client_id, company_id))
                project_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new project type '{description}' with client id {client_id} and company id {company_id} with key: '{project_type_key}'")
                return project_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing project type '{description}' with client id {client_id} and company id {company_id}: {e}")
        raise
