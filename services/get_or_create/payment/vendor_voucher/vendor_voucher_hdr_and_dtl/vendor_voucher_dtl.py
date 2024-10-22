import psycopg2
from utils.logger import logger
from queries.vendor_voucher.vendor_voucher import get_vendor_voucher_dtl, create_vendor_voucher_dtl
from config import CLIENT_ID

client_id = CLIENT_ID


def get_or_create_vendor_voucher_dtl(conn, paid_amount, client_id, invoice_id, voucher_hdr_key):
    if client_id is None:
        client_id = CLIENT_ID

    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve vendor payment voucher detail for invoice ID: {invoice_id}, paid amount: {paid_amount}, client ID: {client_id}, and voucher header key: {voucher_hdr_key}")

            cursor.execute(get_vendor_voucher_dtl, (invoice_id,
                           paid_amount, client_id, voucher_hdr_key))
            result = cursor.fetchone()

            if result:
                voucher_detail_key = result[0]
                logger.info(
                    f"Vendor payment voucher detail found for invoice ID: {invoice_id}, paid amount: {paid_amount}, client ID: {client_id}, and voucher header key: {voucher_hdr_key} with key: {voucher_detail_key}")
                return voucher_detail_key, False
            else:
                logger.info(
                    f"Vendor payment voucher detail not found for invoice ID: {invoice_id}, paid amount: {paid_amount}, client ID: {client_id}, and voucher header key: {voucher_hdr_key}, Creating a new entry.")

                # Insert new voucher detail
                cursor.execute(create_vendor_voucher_dtl,
                               (paid_amount, client_id, invoice_id, voucher_hdr_key))
                voucher_detail_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new vendor payment voucher detail fofor invoice ID: {invoice_id}, paid amount: {paid_amount}, client ID: {client_id}, and voucher header key: {voucher_hdr_key}, with key: {voucher_detail_key}")
                return voucher_detail_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing voucher detail for invoice ID: {invoice_id}, paid amount: {paid_amount}, client ID: {client_id}, and voucher header key: {voucher_hdr_key}: {e}")
        raise
