import psycopg2
from utils.logger import logger
from utils.filter_paid_vendor_po import filter_paid_vendor_po
from utils.vendor_po.get_vendor_po import get_paid_vendor_po_details
from services.get_or_create.payment.vendor_invoice.vendor_invoice import get_or_create_vendor_invoice
from services.get_or_create.payment.vendor_voucher.vendor_voucher import get_or_create_vendor_voucher


def load_vendor_invoice_and_voucher(conn):
    try:
        paid_po_desc_values = filter_paid_vendor_po(conn)
        logger.info(
            f"Filtered Paid Vendor PO Data read: {paid_po_desc_values}")

        # Initialize counters for vendor invoices and vouchers
        invoice_counters = {"created": 0, "existing": 0}
        voucher_counters = {"created": 0, "existing": 0}

        for po_desc, payment_mode in paid_po_desc_values:
            vendor_po = get_paid_vendor_po_details(conn, po_desc)

            if vendor_po:
                PO_Date, PO_NetAmt, PO_Client_ID, PO_Company_ID, PO_Proj_Key, PO_Vend_Key, PO_GstAmt, PO_Key = vendor_po

                # Get or create vendor invoice
                vend_inv_key, created = get_or_create_vendor_invoice(
                    conn, PO_Date, PO_NetAmt, PO_Client_ID, PO_Company_ID, PO_Proj_Key, PO_Vend_Key, PO_GstAmt, PO_Key)

                if created:
                    invoice_counters["created"] += 1
                else:
                    invoice_counters["existing"] += 1

                logger.info(
                    f"The key of the vendor invoice for po_key {PO_Key} is: {vend_inv_key}")

                # Get or create vendor voucher
                vendor_voucher_response = get_or_create_vendor_voucher(
                    conn, PO_Date, PO_NetAmt, PO_Client_ID, PO_Company_ID, PO_Vend_Key, vend_inv_key, PO_NetAmt, payment_mode)

                # Use counters from vendor voucher response
                voucher_counters['created'] += vendor_voucher_response['counters']['voucher_hdr']['created']
                voucher_counters['existing'] += vendor_voucher_response['counters']['voucher_hdr']['existing']

                logger.info(
                    f"The key of the vendor voucher is: {vendor_voucher_response['voucher_hdr_key']}")

        conn.commit()
        logger.info(
            "All operations completed successfully. Transaction committed.")

    except psycopg2.Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise

    except Exception as e:
        conn.rollback()
        logger.error(f"Unexpected error: {e}")
        raise

    finally:
        logger.info("Operation completed.")

    # Return the aggregated counters for invoices and vouchers
    return {
        "vendor invoice": invoice_counters,
        "vendor voucher": voucher_counters
    }
