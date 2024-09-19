import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.vendor.vendor_type import get_vendor_type, create_vendor_type

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_vendor_type(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve vendor type: '{description}' with company ID: '{company_id}'")

            cursor.execute(get_vendor_type, (description, company_id))
            result = cursor.fetchone()

            if result:
                vendor_type_key = result[0]
                logger.info(
                    f"Vendor type '{description}' found with key: '{vendor_type_key}'")
                return vendor_type_key, False
            else:
                logger.info(
                    f"Vendor type '{description}' not found, creating new entry.")

                cursor.execute(create_vendor_type, (description,
                               created_by, created_at, client_id, company_id))
                vendor_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new vendor type '{description}' with key: '{vendor_type_key}'")
                return vendor_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing vendor type '{description}': {e}")
        raise
