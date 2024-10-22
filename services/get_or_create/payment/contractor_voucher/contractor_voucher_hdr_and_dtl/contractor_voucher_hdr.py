import psycopg2
from utils.logger import logger
from utils.get_last_number import get_last_number
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.last_number.contractor.contractor_voucher import get_last_contractor_voucher_number
from queries.contractor_voucher.contractor_voucher import get_contractor_voucher_hdr, create_contractor_voucher_hdr

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_contractor_voucher_hdr(conn, contract_voucher_date, total_amount, client_id, company_id, contractor_key, payment_mode_id):

    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve contract voucher hdr with date: {contract_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, contractor_key: {contractor_key} and payment_mode_id: {payment_mode_id}"
            )
            # Check if the voucher already exists
            cursor.execute(get_contractor_voucher_hdr, (contract_voucher_date,
                           total_amount, client_id, company_id, contractor_key, payment_mode_id))
            result = cursor.fetchone()

            if result:
                contract_voucher_key = result[0]
                logger.info(
                    f"Contract voucher hdr found with key: '{contract_voucher_key}' for date: {contract_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, contractor_key: {contractor_key}, and payment_mode_id: {payment_mode_id}"
                )
                return contract_voucher_key, False
            else:
                # Generate a new voucher number
                last_voucher_number = get_last_number(
                    conn, get_last_contractor_voucher_number, company_id, client_id)
                next_voucher_number = str(last_voucher_number + 1)
                logger.info(
                    f"Contract voucher hdr with date: {contract_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, contractor_key: {contractor_key}, and payment_mode_id: {payment_mode_id} is not found, Creating a new entry."
                )

                # Insert the new contract voucher
                cursor.execute(create_contractor_voucher_hdr,
                               (next_voucher_number, contract_voucher_date, total_amount, client_id, company_id,
                                payment_mode_id, contractor_key))

                contract_voucher_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new contract voucher hdr with date: {contract_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, contractor_key: {contractor_key}, and payment_mode_id: {payment_mode_id}, with key: '{contract_voucher_key}'"
                )
                return contract_voucher_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing contract voucher hdr with date: {contract_voucher_date}, amount: {total_amount}, client_id: {client_id}, company_id: {company_id}, contractor_key: {contractor_key}, and payment_mode_id: {payment_mode_id}: {e}"
        )
        raise
