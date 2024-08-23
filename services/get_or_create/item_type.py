import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item_type import get_item_type, create_item_type

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_type(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item type with description: '{description}'")
            cursor.execute(get_item_type, (description,))
            result = cursor.fetchone()

            if result:
                item_type_key = result[0]
                logger.info(
                    f"Item type '{description}' found with key: '{item_type_key}'")
                return item_type_key, False
            else:
                logger.info(
                    f"Item type '{description}' not found, creating new entry.")
                cursor.execute(create_item_type, (description, created_by,
                               created_at, client_id))
                item_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item type '{description}' with key: '{item_type_key}'")
                return item_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item type '{description}': {e}")
        raise
