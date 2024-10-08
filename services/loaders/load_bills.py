import psycopg2
from utils.logger import logger
from utils.excel_readers.read_bills_data import read_bills_data
from services.get_or_create.vendor.vendor import get_or_create_vendor
from services.get_or_create.project.project import get_or_create_project
from services.get_or_create.bills.purchase_order import get_or_create_purchase_order
from services.get_or_create.bills.purchase_order_items import get_or_create_purchase_order_item
from utils.compare_item_with_excel_and_db import get_or_set_default_item


def load_bills(conn):
    try:
        pairs = read_bills_data()
        logger.info(f"Data read from Excel: {pairs}")

        # Initialize the list to track default vendors and items
        default_vendor_list = []
        default_item_list = []

        # Counters for created, existing, and default items/vendors
        counters = {
            "project": {"created": 0, "existing": 0},
            "vendor": {"created": 0, "existing": 0, "default": 0},
            "purchase order": {"created": 0, "existing": 0},
            "purchase order items": {"created": 0, "existing": 0},
            "item": {"default": 0}  # Counter for default items
        }

        for bill_no, po_date, material_type, vendor, net_amount, gst_amount, project, items in pairs:
            # Get or create the project
            project_key, created = get_or_create_project(conn, project)
            if created:
                counters["project"]["created"] += 1
            else:
                counters["project"]["existing"] += 1

            # Get or create the vendor
            vendor_key, created = get_or_create_vendor(
                conn, vendor, default_vendor=True, default_vendor_list=default_vendor_list)

            if created:
                counters["vendor"]["created"] += 1
            else:
                if vendor in default_vendor_list:
                    counters["vendor"]["default"] += 1
                else:
                    counters["vendor"]["existing"] += 1

            logger.info(f"The key of the vendor '{vendor}' is: '{vendor_key}'")

            # Get or create the purchase order
            po_key, created = get_or_create_purchase_order(
                conn, str(bill_no), po_date, project_key, vendor_key, net_amount, gst_amount)

            if created:
                counters["purchase order"]["created"] += 1
            else:
                counters["purchase order"]["existing"] += 1

            logger.info(
                f"The key of the PO with desc {bill_no}, date {po_date}, net {net_amount} and gst {gst_amount} is {po_key}")

            # Process each item from the items list
            for item in items:
                item_name = item.get('ItemName')

                # Pass default_item_list to track default items
                item_key = get_or_set_default_item(
                    conn, item_name, default_item_list)

                qty = item.get('ItemQuantity') or 1
                if not qty or str(qty).strip() == '':
                    qty = 1
                price = item.get('ItemPrice')

                po_item_key, created = get_or_create_purchase_order_item(
                    conn, item_key, qty, price, po_key)

                if created:
                    counters["purchase order items"]["created"] += 1
                else:
                    counters["purchase order items"]["existing"] += 1

                logger.info(
                    f"The key of the PO item with item key {item_key}, qty {qty} and price {price} is {po_item_key}")

        # Log the final count of default vendors and the list of vendors returned as default
        logger.info(
            f"Number of vendors returned as default: {counters['vendor']['default']}")
        logger.info(f"Vendors returned as default: {default_vendor_list}")

        # Log the final count of default items and the list of items replaced by default
        counters["item"]["default"] = len(default_item_list)
        logger.info(
            f"Number of items replaced with default: {counters['item']['default']}")
        logger.info(f"Items replaced with default: {default_item_list}")

        logger.info(
            f"Purchase order items created: {counters['purchase order items']['created']}")

        # Commit the transaction if all operations were successful
        conn.commit()
        logger.info(
            "All operations completed successfully. Transaction committed.")

    except psycopg2.Error as e:
        # Rollback the transaction in case of any error
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise

    except Exception as e:
        # Rollback in case of any other unforeseen error
        conn.rollback()
        logger.error(f"Unexpected error: {e}")
        raise

    finally:
        logger.info("Operation completed.")

    return counters
