import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from queries.item_purpose.item_purpose import get_item_purpose, create_item_purpose


client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_purpose(conn, item_key, item_descr, purpose_key, purpose):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item purpose for item: '{item_descr}' and purpose: '{purpose}' with client id {client_id}")
            cursor.execute(
                get_item_purpose, (item_key, purpose_key, client_id))
            result = cursor.fetchone()

            if result:
                item_purpose_key = result[0]
                logger.info(
                    f"Item purpose for item: '{item_descr}' and purpose: '{purpose}' with client id {client_id} is found with key: '{item_purpose_key}'")
                created = False
            else:
                logger.info(
                    f"Item purpose for item: '{item_descr}' and purpose: '{purpose}' with client id {client_id} is not found, creating new entry.")
                cursor.execute(create_item_purpose, (item_key, purpose_key, client_id))
                item_purpose_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item purpose for item: '{item_descr}' and purpose: '{purpose}' for client id {client_id} with key: '{item_purpose_key}'")
                created = True

            return item_purpose_key, created

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Item purpose for item: '{item_descr}' and purpose: '{purpose}' with client id {client_id}: {e}")
        raise
