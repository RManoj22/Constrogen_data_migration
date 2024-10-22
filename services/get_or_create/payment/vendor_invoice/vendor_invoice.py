import psycopg2
from utils.logger import logger
from utils.get_last_number import get_last_number
from queries.vendor_po.po_desc import update_vendor_po_status
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.last_number.vendor.vendor_invoice import get_last_vendor_invoice_number
from queries.vendor_invoice.vendor_invoice import get_vendor_invoice, create_vendor_invoice

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_vendor_invoice(conn, PO_Date, PO_NetAmt, PO_Client_ID, PO_Company_ID, PO_Proj_Key, PO_Vend_Key, PO_GstAmt, PO_Key):
    """
    Check if a vendor invoice exists for the provided PO. If not, create a new vendor invoice
    and update the PO's status to 'I'.

    Parameters:
    conn: psycopg2 connection object
    PO_Date: Date of the Purchase Order
    PO_NetAmt: Net amount of the Purchase Order
    PO_Client_ID: ID of the client
    PO_Company_ID: ID of the company
    PO_Proj_Key: Project key associated with the Purchase Order
    PO_Vend_Key: Vendor key associated with the Purchase Order
    PO_GstAmt: GST amount of the Purchase Order
    PO_Key: Key of the Purchase Order

    Returns:
    tuple: (vend_inv_key, created), where vend_inv_key is the key of the vendor invoice
           and created is a boolean indicating whether a new invoice was created.
    """
    try:
        with conn.cursor() as cursor:
            logger.info(f"Attempting to retrieve vendor invoice with PO_Date: {PO_Date}, PO_NetAmt: {PO_NetAmt}, "
                        f"PO_Client_ID: {PO_Client_ID}, PO_Company_ID: {PO_Company_ID}, "
                        f"PO_Proj_Key: {PO_Proj_Key}, PO_Vend_Key: {PO_Vend_Key}, "
                        f"PO_GstAmt: {PO_GstAmt}, and PO_Key: {PO_Key}")

            cursor.execute(get_vendor_invoice, (PO_Date, PO_NetAmt, PO_Client_ID,
                                                PO_Company_ID, PO_Proj_Key, PO_Vend_Key,
                                                PO_GstAmt, PO_Key))
            result = cursor.fetchone()

            if result:
                vend_inv_key = result[0]
                logger.info(
                    f"Vendor invoice for PO_Key {PO_Key} found with key {vend_inv_key}")
                return vend_inv_key, False
            else:
                last_invoice_number = get_last_number(
                    conn, get_last_vendor_invoice_number, company_id, client_id)
                next_invoice_number = str(last_invoice_number + 1)
                logger.info(
                    f"Vendor invoice not found for PO_Key {PO_Key}, creating a new entry.")
                cursor.execute(create_vendor_invoice, (next_invoice_number, PO_Date, PO_NetAmt, 0.00,
                                                       created_by, created_at, PO_Client_ID, PO_Company_ID,
                                                       PO_Proj_Key, PO_Vend_Key, PO_GstAmt, 'FromPO', 0.00,
                                                       PO_Key, 'P', PO_NetAmt))
                vend_inv_key = cursor.fetchone()[0]
                logger.info(
                    f"Vendor invoice for PO_Key {PO_Key} created with VendInv_Key = {vend_inv_key}")

                try:
                    logger.info(
                        f"Attempting to update PO with PO_KEY {PO_Key}'s PO_Status to 'I'")
                    cursor.execute(update_vendor_po_status, (PO_Key,))
                    logger.info(
                        f"Updated PO with PO_KEY {PO_Key}'s PO_Status to 'I'")
                except psycopg2.Error as e:
                    logger.error(
                        f"Database error while updating PO with PO_KEY {PO_Key}'s PO_Status to 'I': {e}")
                    raise

                logger.info(
                    f"Vendor invoice created for PO with PO_KEY {PO_Key} with INVOICE_KEY {vend_inv_key}")
                return vend_inv_key, True
    except psycopg2.Error as e:
        logger.error(f"Database error while processing vendor invoice: {e}")
        raise
