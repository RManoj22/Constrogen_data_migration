from utils.logger import logger
from utils.excel_readers.read_vendor_payments_data import read_vendor_payments_data
from utils.vendor_po.get_all_vendor_po_desc import get_all_vendor_po_desc_func


def filter_paid_vendor_po(conn):
    vendor_po_payment_status = {
        "Paid BilNos": [],
        "Not Paid BilNos": [],
    }
    logger.info(
        "Filtering POs by checking whether the matching PO Desc (BillNo) exists in the payment data")

    # Retrieve BillNos from the database
    db_bill_nos_found = get_all_vendor_po_desc_func(conn)
    logger.info(f"BillNos found in the database: {db_bill_nos_found}")

    # Read payment data from Excel
    payment_data = read_vendor_payments_data()
    logger.info(f"Payment data read from Excel: {payment_data}")

    # Create a dictionary mapping BillNo (as strings) to PaymentMode for easy lookup
    bill_to_payment_mode = {
        str(entry['BillNo']): entry['PaymentMode'] for entry in payment_data
    }

    for db_vendor_po_bill_no in db_bill_nos_found:
        if db_vendor_po_bill_no not in bill_to_payment_mode:
            logger.info(
                f"PO Desc (Bill No): '{db_vendor_po_bill_no}' not found in the payment data")
            vendor_po_payment_status['Not Paid BilNos'].append(
                db_vendor_po_bill_no)
        else:
            payment_mode = bill_to_payment_mode[db_vendor_po_bill_no]
            logger.info(
                f"PO Desc (Bill No): '{db_vendor_po_bill_no}' found in the payment data with Payment Mode: {payment_mode}")
            vendor_po_payment_status['Paid BilNos'].append(
                (db_vendor_po_bill_no, payment_mode))

    logger.info(f"Vendor POs payment status: {vendor_po_payment_status}")
    logger.info(
        f"Returning the paid Vendor POs: {vendor_po_payment_status['Paid BilNos']}")

    return vendor_po_payment_status['Paid BilNos']
