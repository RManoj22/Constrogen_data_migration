import psycopg2
from utils.logger import logger
from queries.uom import get_uom, create_uom
from config import CLIENT_ID, CREATED_BY, CREATED_AT

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_uom(conn, description, item_type_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item UOM with description: '{description}' where item type key is '{item_type_key}'")
            cursor.execute(get_uom, (description, item_type_key))
            result = cursor.fetchone()

            if result:
                uom_key = result[0]
                logger.info(
                    f"Item UOM '{description}' where item type key '{item_type_key}' is found with key: '{uom_key}'")
                return uom_key, False
            else:
                logger.info(
                    f"Item UOM '{description}' not found where item type key is '{item_type_key}', creating new entry.")
                cursor.execute(create_uom, (description, created_by,
                               created_at, client_id, item_type_key))
                uom_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item UOM '{description}' where item type key is '{item_type_key}' with key: '{uom_key}'")
                return uom_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item UOM '{description}' where item type key is '{item_type_key}': {e}")
        raise
