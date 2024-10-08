import psycopg2
from utils.logger import logger
from queries.bills.purchase_order_items import get_purchase_order_item, create_purchase_order_item
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT


client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_purchase_order_item(conn, item_key, qty, price, po_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve PO item with item_key {item_key}, qty {qty}, price {price}, po_key {po_key}, client id {client_id} and company id {company_id}")
            cursor.execute(get_purchase_order_item,
                           (po_key, item_key, price, qty, client_id, company_id))
            result = cursor.fetchone()

            if result:
                purchase_order_item_key = result[0]
                logger.info(
                    f"PO item with item_key {item_key}, qty {qty}, price {price}, po_key {po_key}, client id {client_id} and company id {company_id} found with key {purchase_order_item_key}")
                return purchase_order_item_key, False
            else:
                logger.info(
                    f"PO item not found with item_key {item_key}, qty {qty}, price {price}, po_key {po_key}, client id {client_id} and company id {company_id}. Creating new entry")

                cursor.execute(create_purchase_order_item, (price, po_key, created_by,
                                                            created_at, client_id, company_id, item_key, qty))
                purchase_order_item_key = cursor.fetchone()[0]
                logger.info(
                    f"Created PO item with item_key {item_key}, qty {qty}, price {price}, po_key {po_key}, client id {client_id} and company id {company_id} with key {purchase_order_item_key}")
                return purchase_order_item_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing PO item with item_key {item_key}, qty {qty}, price {price}, po_key {po_key}, client id {client_id} and company id {company_id}: {e}")
        raise
