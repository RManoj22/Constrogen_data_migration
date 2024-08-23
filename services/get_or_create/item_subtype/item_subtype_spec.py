import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item_subtype.item_subtype_spec import get_item_subtype_spec, create_item_subtype_spec

client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_subtype_spec(conn, description, item_subtype_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve Item Subtype Specification: '{description}' where item subtype key is '{item_subtype_key}'")
            cursor.execute(get_item_subtype_spec,
                           (description, item_subtype_key))
            result = cursor.fetchone()

            if result:
                item_subtype_spec_key = result[0]
                logger.info(
                    f"Item Subtype Specification '{description}' where item subtype key '{item_subtype_key}' is found with key: '{item_subtype_spec_key}'")
            else:
                logger.info(
                    f"Item Subtype Specification '{description}' not found where item subtype key is '{item_subtype_key}', creating new entry.")
                cursor.execute(create_item_subtype_spec, (description, created_by,
                               created_at, client_id, item_subtype_key))
                item_subtype_spec_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new Item Subtype Specification '{description}' where item subtype key is '{item_subtype_key}' with key: '{item_subtype_spec_key}'")

            return item_subtype_spec_key

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Item Subtype Specification '{description}' with item subtype key '{item_subtype_key}': {e}")
        raise
