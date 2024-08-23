import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.purpose import get_purpose, create_purpose

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_purpose(conn, purpose, item_type_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve purpose: '{purpose}' with item type key '{item_type_key}'")
            cursor.execute(get_purpose, (purpose, item_type_key))
            result = cursor.fetchone()

            if result:
                purpose_key = result[0]
                logger.info(
                    f"Purpose '{purpose}' found with key: '{purpose_key}'")
                created = False
            else:
                logger.info(
                    f"Purpose '{purpose}' not found with item type key '{item_type_key}', creating new entry.")
                cursor.execute(create_purpose, (purpose, created_by,
                               created_at, client_id, item_type_key))
                purpose_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new purpose '{purpose}' with key: '{purpose_key}' for item type key '{item_type_key}'")
                created = True

            return purpose_key, created

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing purpose '{purpose}' with item type key '{item_type_key}': {e}")
        raise
