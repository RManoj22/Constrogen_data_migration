from utils.logger import logger
from utils.read_excel import read_excel
from database.db_connection import get_db_connection
from services.get_or_create.uom import get_or_create_uom
from services.get_or_create.purpose import get_or_create_purpose
from services.get_or_create.item_type import get_or_create_item_type
from services.get_or_create.item_subtype.item_subtype import get_or_create_item_subtype
from services.get_or_create.item.item import get_or_create_item


if __name__ == "__main__":
    logger.info("Starting the application")

    conn = get_db_connection()
    if conn:
        try:
            logger.info("Successfully connected to the database")
            conn.autocommit = False

            pairs = read_excel()
            logger.info(f"Data read from Excel: {pairs}")

            item_type_keys = {}
            uom_keys = {}

            counters = {
                "item_type": {"created": 0, "existing": 0},
                "uom": {"created": 0, "existing": 0},
                "purpose": {"created": 0, "existing": 0},
                "item_subtype": {"created": 0, "existing": 0},
                "item": {"created": 0, "existing": 0}
            }

            try:
                for item_type_descr, item_subtype_descr, item_descr, purpose, uom, item_subtype_gst, item_subtype_spec in pairs:
                    if item_type_descr not in item_type_keys:
                        item_type_key, created = get_or_create_item_type(
                            conn, item_type_descr)
                        item_type_keys[item_type_descr] = item_type_key
                        if created:
                            counters["item_type"]["created"] += 1
                        else:
                            counters["item_type"]["existing"] += 1
                        logger.info(
                            f"The key of the item type '{item_type_descr}' is: '{item_type_key}'")
                    else:
                        item_type_key = item_type_keys[item_type_descr]

                    uom_keys[item_type_key] = []
                    for uom_in in uom:
                        uom_key, created = get_or_create_uom(
                            conn, uom_in, item_type_key)
                        uom_keys[item_type_key].append(uom_key)
                        if created:
                            counters["uom"]["created"] += 1
                        else:
                            counters["uom"]["existing"] += 1
                        logger.info(
                            f"The key of the uom '{uom_in}' where item type '{item_type_descr}' is: '{uom_key}'")

                    item_subtype_key, item_subtype_spec_keys, created = get_or_create_item_subtype(
                        conn, item_subtype_descr, item_type_key, uom_keys[item_type_key], item_subtype_gst, item_subtype_spec)
                    if created:
                        counters["item_subtype"]["created"] += 1
                    else:
                        counters["item_subtype"]["existing"] += 1
                    logger.info(
                        f"The key of the item sub type '{item_subtype_descr}' with GST '{item_subtype_gst}' is: '{item_subtype_key}'")

                    purpose_key, created = get_or_create_purpose(
                        conn, purpose, item_type_key)
                    if created:
                        counters["purpose"]["created"] += 1
                    else:
                        counters["purpose"]["existing"] += 1
                    logger.info(
                        f"The key of the purpose '{purpose}' where item type '{item_type_descr}' is: '{purpose_key}'")

                    item_key, created = get_or_create_item(
                        conn, item_descr, item_subtype_gst, item_type_key, item_subtype_key, purpose_key, item_subtype_spec_keys[item_subtype_key], item_subtype_spec, uom_keys[item_type_key])
                    if created:
                        counters["item"]["created"] += 1
                    else:
                        counters["item"]["existing"] += 1
                    logger.info(
                        f"The key of the item '{item_descr}' where item type '{item_type_descr}' is: '{item_key}'")

                conn.commit()
                logger.info(
                    "All operations completed successfully. Transaction committed.")

                for service, count in counters.items():
                    logger.info(
                        f"{service.capitalize()} - Created: {count['created']}, Existing: {count['existing']}")

            except Exception as e:
                conn.rollback()
                logger.error(f"An error occurred during operations: {e}")
                raise

        except Exception as e:
            logger.error(f"An error occurred: {e}")

        finally:
            conn.close()
            logger.info("Database connection closed")
