import psycopg2
from utils.logger import logger
from services.get_or_create.project.project import get_or_create_project
from services.get_or_create.contractor.contractor import get_or_create_contractor
from utils.excel_readers.read_contractor_payments_data import read_contractor_payments_data
from services.get_or_create.payment.contractor_voucher.contractor_voucher import get_or_create_contractor_voucher
from services.get_or_create.payment.contractor_invoice.contractor_invoice import get_or_create_contractor_invoice
from config import CLIENT_ID, COMPANY_ID

client_id = CLIENT_ID
company_id = COMPANY_ID


def load_contractor_invoice_and_voucher(conn):
    try:
        # Filter the contractor data to process
        contractor_payment_data = read_contractor_payments_data()
        logger.info(f"contractor Payment Data read: {contractor_payment_data}")

        # Initialize counters for contractor invoices and vouchers
        invoice_project = {"created": 0, "existing": 0}
        invoice_contractor = {"created": 0, "existing": 0}
        invoice_counters = {"created": 0, "existing": 0}
        voucher_counters = {"created": 0, "existing": 0}

        for payment_date, project_name, contractor_name, contractor_amount in contractor_payment_data:
            # Get or create project
            project_key, created = get_or_create_project(
                conn, project_name)

            if created:
                invoice_project["created"] += 1
            else:
                invoice_project["existing"] += 1

            logger.info(
                f"The key of the project {project_name} is: {project_key}")

            # Get or create contractor
            contractor_key, created = get_or_create_contractor(
                conn, contractor_name, client_id, company_id)

            if created:
                invoice_contractor["created"] += 1
            else:
                invoice_contractor["existing"] += 1

            logger.info(
                f"The key of the contractor {contractor_name} is: {contractor_key}")

            # Get or create contractor invoice
            contractor_inv_key, created = get_or_create_contractor_invoice(
                conn, payment_date, contractor_amount, project_key, contractor_key, client_id, company_id)

            if created:
                invoice_counters["created"] += 1
            else:
                invoice_counters["existing"] += 1

            logger.info(
                f"The key of the contractor invoice with date {payment_date}, amount {contractor_amount}, project key {project_key}, contractor key {contractor_key}, client id {client_id} and company id {company_id} is: {contractor_inv_key}")

            # Get or create contractor voucher
            contractor_voucher_response = get_or_create_contractor_voucher(
                conn, payment_date, contractor_key, contractor_amount, contractor_inv_key, client_id, company_id)

            # Use counters from contractor voucher response
            voucher_counters['created'] += contractor_voucher_response['counters']['voucher_hdr']['created']
            voucher_counters['existing'] += contractor_voucher_response['counters']['voucher_hdr']['existing']

            logger.info(
                f"The key of the contractor voucher is: {contractor_voucher_response['voucher_hdr_key']}")

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
        "contractor invoice": invoice_counters,
        "contractor voucher": voucher_counters
    }
