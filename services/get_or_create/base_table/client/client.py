import psycopg2
from utils.logger import logger
from queries.base_table.client.client import get_client, create_client


def get_or_create_client(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve client: '{description}'")
            cursor.execute(get_client, (description,))
            result = cursor.fetchone()

            if result:
                client_id = result[0]
                logger.info(
                    f"Client'{description}' found with ID: '{client_id}'")
                return client_id, False
            else:
                logger.info(
                    f"Client '{description}' not found, creating new entry.")
                cursor.execute(create_client, (description,))
                client_id = cursor.fetchone()[0]
                logger.info(
                    f"Created new client '{description}' with ID: '{client_id}'")
                return client_id, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Client '{description}': {e}")
        raise
