import psycopg2
from utils.logger import logger
from queries.vendor_po.po_desc import get_vendor_po_details


def get_paid_vendor_po_details(conn, po_desc):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve Vendor PO where PO_Desc is {po_desc}")
            cursor.execute(get_vendor_po_details, (po_desc,))
            result = cursor.fetchone()

            if result:
                PO_Date, PO_NetAmt, PO_Client_ID, PO_Company_ID, PO_Proj_Key, PO_Vend_Key, PO_GstAmt, PO_Key = result
                logger.info(
                    f"Vendor PO with PO_Desc {po_desc} found with key {PO_Key}, Returning Vendor PO Details: {result}")
                return result
            else:
                logger.warning(
                    f"No Vendor PO found with PO_Desc {po_desc}. Returning None.")
                return None

    except psycopg2.Error as e:
        logger.error(
            f"Database error while retrieving Vendor PO where PO_Desc is {po_desc}: {e}")
        raise
