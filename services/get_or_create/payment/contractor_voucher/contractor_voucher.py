import psycopg2
from utils.logger import logger
from ..mode_of_pay.mode_of_pay import get_or_create_mode_of_pay
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT, CONTRACTOR_PAYMENT_MODE
from queries.contractor_invoice.contractor_invoice import update_contractor_invoice_status
from .contractor_voucher_hdr_and_dtl.contractor_voucher_dtl import get_or_create_contractor_voucher_dtl
from services.get_or_create.payment.contractor_voucher.contractor_voucher_hdr_and_dtl.contractor_voucher_hdr import get_or_create_contractor_voucher_hdr

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


payment_mode = CONTRACTOR_PAYMENT_MODE


def get_or_create_contractor_voucher(conn, voucher_date, contractor_key, total_amount,
                                     invoice_key, client_id, company_id):
    counters = {
        'mode_of_pay': {'created': 0, 'existing': 0},
        'voucher_hdr': {'created': 0, 'existing': 0},
        'voucher_dtl': {'created': 0, 'existing': 0}
    }

    try:
        # Get or create mode of payment
        mode_of_pay_key, mode_of_pay_created = get_or_create_mode_of_pay(
            conn, payment_mode)
        counters['mode_of_pay']['created' if mode_of_pay_created else 'existing'] += 1

        # Get or create contractor voucher header
        voucher_hdr_key, hdr_created = get_or_create_contractor_voucher_hdr(
            conn, voucher_date, total_amount, client_id, company_id, contractor_key, mode_of_pay_key)
        counters['voucher_hdr']['created' if hdr_created else 'existing'] += 1

        # Get or create contractor voucher detail
        voucher_dtl_key, dtl_created = get_or_create_contractor_voucher_dtl(
            conn, total_amount, client_id, invoice_key, voucher_hdr_key)
        counters['voucher_dtl']['created' if dtl_created else 'existing'] += 1

        logger.info(
            f"Contractor Voucher header created: {hdr_created}, Voucher detail created: {dtl_created}")

        # If both header and detail are created, update the contractor invoice status to 'P'
        if hdr_created and dtl_created:
            try:
                logger.info(
                    f"Attempting to update contractor invoice status to 'P' for invoice_key: {invoice_key}")
                cursor = conn.cursor()
                cursor.execute(
                    update_contractor_invoice_status, (invoice_key,))
                logger.info(
                    f"Successfully updated contractor invoice status to 'P' for invoice_key: {invoice_key}")
            except psycopg2.Error as e:
                logger.error(
                    f"Error updating contractor invoice status for invoice_key: {invoice_key}: {e}")
                raise

    except Exception as e:
        logger.error(f"Error processing contractor voucher: {e}")
        raise

    # Log counters after all operations
    logger.info(f"Mode of Pay - Created: {counters['mode_of_pay']['created']}, "
                f"Existing: {counters['mode_of_pay']['existing']}")
    logger.info(f"Contractor Voucher Header - Created: {counters['voucher_hdr']['created']}, "
                f"Existing: {counters['voucher_hdr']['existing']}")
    logger.info(f"Contractor Voucher Detail - Created: {counters['voucher_dtl']['created']}, "
                f"Existing: {counters['voucher_dtl']['existing']}")

    return {
        'voucher_hdr_key': voucher_hdr_key,
        'voucher_dtl_key': voucher_dtl_key,
        'counters': counters
    }
