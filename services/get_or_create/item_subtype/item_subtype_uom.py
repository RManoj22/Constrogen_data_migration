import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item_subtype.item_subtype_uom import get_item_subtype_uom, create_item_subtype_uom

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_subtype_uom(conn, item_uom_key, item_subtype_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve Item Subtype UOM where item subtype key is '{item_subtype_key}' and item UOM key is '{item_uom_key}'")
            cursor.execute(get_item_subtype_uom,
                           (item_subtype_key, item_uom_key))
            result = cursor.fetchone()

            if result:
                item_subtype_uom_key = result[0]
                logger.info(
                    f"Item Subtype UOM found with key: '{item_subtype_uom_key}' for item subtype key '{item_subtype_key}' and item UOM key '{item_uom_key}'")
            else:
                logger.info(
                    f"Item Subtype UOM not found, creating new entry for item subtype key '{item_subtype_key}' and item UOM key '{item_uom_key}'.")
                cursor.execute(create_item_subtype_uom, (created_by, created_at,
                                                         client_id, item_subtype_key, item_uom_key))
                item_subtype_uom_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new Item Subtype UOM with key: '{item_subtype_uom_key}' for item subtype key '{item_subtype_key}' and item UOM key '{item_uom_key}'")

            return item_subtype_uom_key

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Item Subtype UOM for item subtype key '{item_subtype_key}' and item UOM key '{item_uom_key}': {e}")
        raise
