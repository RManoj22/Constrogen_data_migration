import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.vendor.vendor_item_type import get_vendor_item_type, create_vendor_item_type

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_vendor_item_type(conn, vendor_key, item_type_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve vendor item type with vendor key: '{vendor_key}' and item type key: '{item_type_key}'")

            cursor.execute(get_vendor_item_type,
                            (vendor_key, item_type_key))
            result = cursor.fetchone()

            if result:
                vendor_item_type_key = result[0]
                logger.info(
                    f"Vendor item type with vendor key '{vendor_key}' and item type key '{item_type_key}' found with key: '{vendor_item_type_key}'")
                return vendor_item_type_key, False
            else:
                logger.info(
                    f"Vendor item type with vendor key '{vendor_key}' and item type key '{item_type_key}' not found, creating new entry.")

                cursor.execute(create_vendor_item_type,
                                (vendor_key, item_type_key, client_id, company_id))
                vendor_item_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new vendor item type for vendor key '{vendor_key}' and item type key '{item_type_key}' with key: '{vendor_item_type_key}'")
                return vendor_item_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing vendor item type with vendor key '{vendor_key}' and item type key '{item_type_key}': {e}")
        raise
