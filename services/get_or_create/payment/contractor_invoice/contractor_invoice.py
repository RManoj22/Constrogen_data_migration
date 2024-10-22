import psycopg2
from utils.logger import logger
from utils.get_last_number import get_last_number
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.last_number.contractor.contractor_invoice import get_last_contractor_invoice_number
from queries.contractor_invoice.contractor_invoice import get_contractor_invoice, create_contractor_invoice
from utils.calculate_tds_amount import calculate_tds_amount

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_contractor_invoice(conn, invoice_date, invoice_amount, project_key, contractor_key, client_id, company_id):
    """
    Check if a contractor invoice exists for the provided InvoiceID. If not, create a new contractor invoice.

    Parameters:
    conn: psycopg2 connection object
    invoice_date: Date of the invoice
    invoice_amount: Total amount of the invoice
    project_key: ID of the project associated with the invoice
    contractor_key: ID of the contractor associated with the invoice
    client_id: ID of the client
    company_id: ID of the company

    Returns:
    tuple: (contractor_inv_key, created), where contractor_inv_key is the key of the contractor invoice
           and created is a boolean indicating whether a new invoice was created.
    """
    try:
        logger.info(
            f"Calling the tds amount calculation function for the invoice amount {invoice_amount}")
        tds_amount = calculate_tds_amount(invoice_amount)
        logger.info(
            f"Tds calculated for the amount {invoice_amount}, passing the value {tds_amount}")
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve contractor invoice with date: {invoice_date}, amount {invoice_amount}, "
                f"Tds amount {tds_amount}, client id {client_id}, company id {company_id}, project key {project_key} "
                f"and contractor key {contractor_key}"
            )

            cursor.execute(get_contractor_invoice,
                           (invoice_date, invoice_amount, tds_amount, client_id, company_id, project_key, contractor_key))
            result = cursor.fetchone()

            if result:
                contractor_inv_key = result[0]
                logger.info(
                    f"Contractor invoice with with date: {invoice_date}, amount {invoice_amount}, Tds amount {tds_amount},"
                    f"client id {client_id}, company id {company_id}, project key {project_key} and contractor key {contractor_key}. found with key {contractor_inv_key}")
                return contractor_inv_key, False
            else:
                last_invoice_number = get_last_number(
                    conn, get_last_contractor_invoice_number, company_id, client_id)
                next_invoice_number = str(last_invoice_number + 1)
                logger.info(
                    f"Contractor invoice with with with date: {invoice_date}, amount {invoice_amount}, Tds amount {tds_amount},"
                    f"client id {client_id}, company id {company_id}, project key {project_key} and contractor key {contractor_key} is not found, creating a new entry.")
                cursor.execute(create_contractor_invoice, (next_invoice_number, invoice_date, invoice_amount, tds_amount,
                                                           "N", client_id, company_id, project_key,
                                                           invoice_amount, contractor_key, "O"))
                contractor_inv_key = cursor.fetchone()[0]
                logger.info(
                    f"Contractor invoice with with with date: {invoice_date}, amount {invoice_amount}, Tds amount {tds_amount},"
                    f"client id {client_id}, company id {company_id}, project key {project_key} and contractor key {contractor_key}. created with Key {contractor_inv_key}")

                return contractor_inv_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing contractor invoice with with with date: {invoice_date}, amount {invoice_amount}, Tds amount {tds_amount}, client id {client_id}, company id {company_id}, project key {project_key} and contractor key {contractor_key}.: {e}")
        raise
