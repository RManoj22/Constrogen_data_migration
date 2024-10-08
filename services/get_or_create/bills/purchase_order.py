import psycopg2
from utils.logger import logger
from queries.bills.purchase_order import get_purchase_order, create_purchase_order
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT


client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_last_po_number(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT "PO_Number" FROM "PurchaseOrder"
                WHERE "PO_Company_ID" = %s AND "PO_Client_ID" = %s
                ORDER BY "PO_Key" DESC LIMIT 1
            """, (company_id, client_id))
            result = cursor.fetchone()
            # Start from 1000 to increment to 1001 later
            return int(result[0]) if result else 1000
    except psycopg2.Error as e:
        logger.error(f"Error fetching the last PO number: {e}")
        raise


def get_or_create_purchase_order(conn,
                                 bill_no, po_date, project_key, vendor_key, net_amount, gst_amount):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve PO with project_key {project_key}, vendor_key {vendor_key}, desc {bill_no}, date {po_date}, net {net_amount}, gst {gst_amount}, client id {client_id} and company id {company_id}")
            cursor.execute(get_purchase_order,
                           (bill_no, po_date, net_amount, gst_amount, vendor_key, project_key, client_id, company_id))
            result = cursor.fetchone()

            if result:
                purchase_order_key = result[0]
                logger.info(
                    f"PO with project_key {project_key}, vendor_key {vendor_key}, desc {bill_no}, date {po_date}, net {net_amount}, gst {gst_amount}, client id {client_id} and company id {company_id} found with key {purchase_order_key}")
                return purchase_order_key, False
            else:
                last_po_number = get_last_po_number(conn)
                next_po_number = str(last_po_number + 1)

                logger.info(
                    f"PO not found with project_key {project_key}, vendor_key {vendor_key}, desc {bill_no}, date {po_date}, net {net_amount}, gst {gst_amount}, client id {client_id}, and company id {company_id}. Creating new entry")

                cursor.execute(create_purchase_order, (next_po_number, bill_no, po_date, created_by,
                                                       created_at, client_id, company_id, project_key, vendor_key, gst_amount, net_amount, 'O', 0.00))
                purchase_order_key = cursor.fetchone()[0]
                logger.info(
                    f"Created PO with PO_Number {next_po_number}, project_key {project_key}, vendor_key {vendor_key}, desc {bill_no}, date {po_date}, net {net_amount}, gst {gst_amount}, client id {client_id} and company id {company_id} with key {purchase_order_key}")
                return purchase_order_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing PO with project_key {project_key}, vendor_key {vendor_key}, desc {bill_no}, date{po_date}, net {net_amount}, gst {gst_amount}, client id {client_id} and company id {company_id}: {e}")
        raise
