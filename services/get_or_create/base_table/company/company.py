import psycopg2
from utils.logger import logger
from queries.base_table.company.company import get_company, create_company


def get_or_create_company(conn, description, client_id):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to company: '{description}' with client id {client_id}")
            cursor.execute(get_company, (description, client_id))
            result = cursor.fetchone()

            if result:
                company_id = result[0]
                logger.info(
                    f"Company'{description}' with client id {client_id} found with ID: '{company_id}'")
                return company_id, False
            else:
                logger.info(
                    f"Company '{description}' with client id {client_id} not found, creating new entry.")
                cursor.execute(create_company, (description, client_id))
                company_id = cursor.fetchone()[0]
                logger.info(
                    f"Created new company '{description}' with client id {client_id} with ID: '{company_id}'")
                return company_id, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing company '{description}' with client id {client_id}: {e}")
        raise
