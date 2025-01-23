import psycopg2
from utils.logger import logger
from queries.vendor.vendor import get_vendor, create_vendor
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT, DEFAULT_VENDOR_KEY

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT
default_vendor_key = DEFAULT_VENDOR_KEY


def get_or_create_vendor(conn, name, state_key=None, city_key=None):

    try:
        with conn.cursor() as cursor:
            logger.info(f"Attempting to retrieve vendor: '{name}'")

            cursor.execute(get_vendor, (name,))
            result = cursor.fetchone()

            if result:
                vendor_key = result[0]
                logger.info(
                    f"Vendor with ID '{name}' found with key: '{vendor_key}'")
                return vendor_key, False
            else:

                logger.info(f"Vendor '{name}' not found, creating new entry.")

                cursor.execute(create_vendor, (name, created_by, created_at,
                               city_key, client_id, company_id, state_key))
                vendor_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new vendor '{name}' with key: '{vendor_key}'")
                return vendor_key, True

    except psycopg2.Error as e:
        logger.error(f"Database error while processing vendor '{name}': {e}")
        raise
