import psycopg2
from utils.logger import logger
from config import CLIENT_ID, CREATED_BY, CREATED_AT
from .item_subtype_uom import get_or_create_item_subtype_uom
from .item_subtype_spec import get_or_create_item_subtype_spec
from queries.item_subtype.item_subtype import get_item_subtype, create_item_subtype


client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_item_subtype(conn, item_subtype_descr, item_type_key, uom_keys, item_subtype_gst, item_subtype_spec):
    item_subtype_spec_keys = {}

    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve item sub type with description: '{item_subtype_descr}' and gst '{item_subtype_gst}' where item type key is '{item_type_key}'")
            cursor.execute(get_item_subtype, (item_subtype_descr,
                                              item_subtype_gst, item_type_key))
            result = cursor.fetchone()

            if result:
                item_subtype_key = result[0]
                logger.info(
                    f"Item sub type '{item_subtype_descr}' of gst '{item_subtype_gst}' where item type key '{item_type_key}' is found with key: '{item_subtype_key}'")
                created = False
            else:
                logger.info(
                    f"Item sub type '{item_subtype_descr}' of gst '{item_subtype_gst}' not found where item type key is '{item_type_key}', creating new entry.")
                cursor.execute(create_item_subtype, (item_subtype_descr, item_subtype_gst, created_by,
                                                     created_at, client_id, item_type_key))
                item_subtype_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new item sub type '{item_subtype_descr}' with gst '{item_subtype_gst}' for item type key '{item_type_key}' with key: {item_subtype_key}")
                created = True

            if item_subtype_key:
                item_subtype_spec_keys[item_subtype_key] = []

                if item_subtype_spec:
                    for spec in item_subtype_spec:
                        item_subtype_spec_key = get_or_create_item_subtype_spec(
                            conn, spec, item_subtype_key)
                        item_subtype_spec_keys[item_subtype_key].append(
                            item_subtype_spec_key)

                for uom in uom_keys:
                    get_or_create_item_subtype_uom(
                        conn, uom, item_subtype_key)

                return item_subtype_key, item_subtype_spec_keys, created

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing item sub type '{item_subtype_descr}' with item type key '{item_type_key}': {e}")
        raise
