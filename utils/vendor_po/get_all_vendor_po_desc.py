import psycopg2
from utils.logger import logger
from queries.vendor_po.po_desc import get_vendor_po_desc


def get_all_vendor_po_desc_func(conn):
    try:
        with conn.cursor() as cursor:
            logger.info("Attempting to retrieve PO Desc from Vendor PO")
            cursor.execute(get_vendor_po_desc)
            results = cursor.fetchall()

            if results:
                logger.info(f"Found {len(results)} PO Desc(s) from Vendor PO")
                return [row[0] for row in results]
            else:
                logger.warning("No PO Desc found. Returning an empty list.")
                return []

    except psycopg2.Error as e:
        logger.error(
            f"Database error while retrieving PO Desc from Vendor PO: {e}")
        raise
