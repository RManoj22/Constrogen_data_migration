import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item.item_uom import get_item_uom, create_item_uom

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_uom(conn, item_key, item_uom_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item UOM relation for item key: '{item_key}' and UOM key: '{item_uom_key}'")
            cursor.execute(get_item_uom, (item_key, item_uom_key))
            result = cursor.fetchone()

            if result:
                item_itemuom_key = result[0]
                logger.info(
                    f"Item UOM relation found for item key: '{item_key}' and UOM key: '{item_uom_key}' with key: '{item_itemuom_key}'")
            else:
                logger.info(
                    f"Item UOM relation not found for item key: '{item_key}' and UOM key: '{item_uom_key}', creating new entry.")
                cursor.execute(create_item_uom, (created_by,
                               created_at, client_id, item_key, item_uom_key))
                item_itemuom_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item UOM relation for item key: '{item_key}' and UOM key: '{item_uom_key}' with key: '{item_itemuom_key}'")
            return item_itemuom_key

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item UOM relation for item key '{item_key}' and UOM key '{item_uom_key}': {e}")
        raise
