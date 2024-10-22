from utils.logger import logger
from .vendor_voucher_hdr_and_dtl.vendor_voucher_hdr import get_or_create_vendor_voucher_hdr
from .vendor_voucher_hdr_and_dtl.vendor_voucher_dtl import get_or_create_vendor_voucher_dtl
from ..mode_of_pay.mode_of_pay import get_or_create_mode_of_pay


def get_or_create_vendor_voucher(conn, voucher_date, total_amount, client_id, company_id, vendor_key,
                                 invoice_id, paid_amount, payment_mode):
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

        # Get or create vendor voucher header
        voucher_hdr_key, hdr_created = get_or_create_vendor_voucher_hdr(
            conn, voucher_date, total_amount, client_id, company_id, vendor_key, mode_of_pay_key)
        counters['voucher_hdr']['created' if hdr_created else 'existing'] += 1

        # Get or create vendor voucher detail
        voucher_dtl_key, dtl_created = get_or_create_vendor_voucher_dtl(
            conn, paid_amount, client_id, invoice_id, voucher_hdr_key)
        counters['voucher_dtl']['created' if dtl_created else 'existing'] += 1

        logger.info(
            f"Voucher header created: {hdr_created}, Voucher detail created: {dtl_created}")

    except Exception as e:
        logger.error(f"Error processing voucher: {e}")
        raise

    # Log counters after all operations
    logger.info(f"Mode of Pay - Created: {counters['mode_of_pay']['created']}, "
                f"Existing: {counters['mode_of_pay']['existing']}")
    logger.info(f"Voucher Header - Created: {counters['voucher_hdr']['created']}, "
                f"Existing: {counters['voucher_hdr']['existing']}")
    logger.info(f"Voucher Detail - Created: {counters['voucher_dtl']['created']}, "
                f"Existing: {counters['voucher_dtl']['existing']}")

    return {
        'voucher_hdr_key': voucher_hdr_key,
        'voucher_dtl_key': voucher_dtl_key,
        'counters': counters
    }
