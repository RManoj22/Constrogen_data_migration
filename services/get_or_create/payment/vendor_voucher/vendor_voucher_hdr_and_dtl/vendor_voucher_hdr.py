import psycopg2
from utils.logger import logger
from utils.get_last_number import get_last_number
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.last_number.vendor.vendor_voucher import get_last_vendor_voucher_number
from queries.vendor_voucher.vendor_voucher import get_vendor_voucher_hdr, create_vendor_voucher_hdr

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_vendor_voucher_hdr(conn, vendor_voucher_date, total_amount, client_id, company_id, vendor_key, mode_of_pay_key):

    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve vendor voucher hdr with date: {vendor_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, vendor_key: {vendor_key} and mode_of_pay_key: {mode_of_pay_key}")

            cursor.execute(get_vendor_voucher_hdr, (vendor_voucher_date,
                           total_amount, client_id, company_id, vendor_key, mode_of_pay_key))
            result = cursor.fetchone()

            if result:
                voucher_hdr_key = result[0]
                logger.info(
                    f"Vendor voucher hdr with date: {vendor_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, vendor_key: {vendor_key} and mode_of_pay_key: {mode_of_pay_key}, found with key: '{voucher_hdr_key}'")
                return voucher_hdr_key, False
            else:
                last_voucher_number = get_last_number(
                    conn, get_last_vendor_voucher_number, company_id, client_id)
                next_voucher_number = str(last_voucher_number + 1)
                logger.info(
                    f"Vendor voucher hdr with date: {vendor_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, vendor_key: {vendor_key} and mode_of_pay_key: {mode_of_pay_key} not found, creating new entry.")

                cursor.execute(create_vendor_voucher_hdr,
                               (next_voucher_number, vendor_voucher_date,
                                total_amount, client_id, company_id, mode_of_pay_key, vendor_key))
                voucher_hdr_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new vendor voucher hdr with date: {vendor_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, vendor_key: {vendor_key} and mode_of_pay_key: {mode_of_pay_key}, with key: '{voucher_hdr_key}'")
                return voucher_hdr_key, True
    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing vendor voucher hdr with date: {vendor_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, vendor_key: {vendor_key} and mode_of_pay_key: {mode_of_pay_key}: {e}")
        raise
