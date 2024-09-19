import psycopg2
from utils.logger import logger
from .item_spec import get_or_create_item_spec
from .item_uom import get_or_create_item_uom
from queries.item.item import get_item, create_item
from config import CLIENT_ID, CREATED_BY, CREATED_AT


client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item(conn, item_descr, gst, item_type_key, item_subtype_key, purpose_key, item_subtype_spec_keys, item_subtype_spec, uom_keys):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item with description: '{item_descr}', item type key: '{item_type_key}', and subtype key: '{item_subtype_key}'")
            cursor.execute(
                get_item, (item_descr, item_type_key, item_subtype_key, purpose_key))
            result = cursor.fetchone()

            if result:
                item_key = result[0]
                logger.info(
                    f"Item '{item_descr}' where item type key: '{item_type_key}', and subtype key: '{item_subtype_key}' is found with key: '{item_key}'")
                created = False
            else:
                logger.info(
                    f"Item '{item_descr}' where item type key: '{item_type_key}', and subtype key: '{item_subtype_key}' is not found, creating new entry.")
                cursor.execute(create_item, (item_descr, 'I', gst, created_by,
                               created_at, client_id, item_type_key, item_subtype_key, purpose_key))
                item_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item '{item_descr}' where item type key: '{item_type_key}', and subtype key: '{item_subtype_key}' with key: '{item_key}'")
                created = True

            if item_key:
                if item_subtype_spec_keys:
                    for spec_key, (dict_key, spec_val) in zip(item_subtype_spec_keys, item_subtype_spec.items()):
                        get_or_create_item_spec(
                            conn, spec_key, spec_val, item_key)

                for uom in uom_keys:
                    get_or_create_item_uom(conn, item_key, uom)

            return item_key, created

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item '{item_descr}' where item type key: '{item_type_key}', and subtype key: '{item_subtype_key}': {e}")
        raise
