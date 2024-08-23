import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item.item_spec import get_item_spec, create_item_spec

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_spec(conn, item_subtype_spec_key, item_spec_value, item_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item specification with value: '{item_spec_value}' for item key: '{item_key}' and item subtype spec key: '{item_subtype_spec_key}'")
            cursor.execute(get_item_spec,
                           (item_spec_value, item_key, item_subtype_spec_key))
            result = cursor.fetchone()

            if result:
                item_spec_key = result[0]
                logger.info(
                    f"Item specification value '{item_spec_value}' for item key: '{item_key}' and item subtype spec key: '{item_subtype_spec_key}' found with key: '{item_spec_key}'")
            else:
                logger.info(
                    f"Item specification value '{item_spec_value}' for item key: '{item_key}' and item subtype spec key: '{item_subtype_spec_key}' not found, creating new entry.")
                cursor.execute(create_item_spec, (item_spec_value, created_by,
                               created_at, client_id, item_key, item_subtype_spec_key))
                item_spec_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item specification '{item_spec_value}' for item key: '{item_key}' and item subtype spec key: '{item_subtype_spec_key}' with key: '{item_spec_key}'")
            return item_spec_key

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item specification '{item_spec_value}' for item key '{item_key}': {e}")
        raise
