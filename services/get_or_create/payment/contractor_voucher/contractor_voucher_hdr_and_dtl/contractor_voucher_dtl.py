import psycopg2
from utils.logger import logger
from queries.contractor_voucher.contractor_voucher import get_contractor_voucher_dtl, create_contractor_voucher_dtl
from config import CLIENT_ID

client_id = CLIENT_ID


def get_or_create_contractor_voucher_dtl(conn, paid_amount, client_id, invoice_key, contract_voucher_hdr_key):
    if client_id is None:
        client_id = CLIENT_ID

    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve contractor voucher detail for Invoice key: '{invoice_key}', "
                f"Paid Amount: '{paid_amount}', Client ID: '{client_id}', and contractor Voucher Header Key: '{contract_voucher_hdr_key}'"
            )

            # Execute the select query to check if the detail already exists
            cursor.execute(get_contractor_voucher_dtl, (invoice_key,
                           paid_amount, client_id, contract_voucher_hdr_key))
            result = cursor.fetchone()

            if result:
                contract_voucher_dtl_key = result[0]
                logger.info(
                    f"contractor voucher detail found for Invoice Key: '{invoice_key}', Paid Amount: '{paid_amount}', "
                    f"Client ID: '{client_id}', and contractor Voucher Header Key: '{contract_voucher_hdr_key}' with key: '{contract_voucher_dtl_key}'"
                )
                return contract_voucher_dtl_key, False
            else:
                logger.info(
                    f"contractor voucher detail not found for Invoice Key: '{invoice_key}', Paid Amount: '{paid_amount}', "
                    f"Client ID: '{client_id}', and contractor Voucher Header Key: '{contract_voucher_hdr_key}', creating new entry."
                )

                # Insert new contractor voucher detail
                cursor.execute(create_contractor_voucher_dtl,
                               (paid_amount, contract_voucher_hdr_key, invoice_key, client_id))
                contract_voucher_dtl_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new contractor voucher detail for Invoice Key '{invoice_key}', paid amount {paid_amount}, hdr key {contract_voucher_hdr_key} with key: '{contract_voucher_dtl_key}'"
                )
                return contract_voucher_dtl_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing contractor voucher detail for Invoice Key '{invoice_key}',"
            f"Client ID: '{client_id}', and contractor Voucher Header Key: '{contract_voucher_hdr_key}': {e}"
        )
        raise
