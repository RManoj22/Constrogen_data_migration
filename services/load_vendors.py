from utils.logger import logger
from utils.excel_readers.read_vendors_data import read_vendors_data
from services.get_or_create.location.city import get_or_create_city
from services.get_or_create.location.state import get_or_create_state
from services.get_or_create.vendor.vendor import get_or_create_vendor
from services.get_or_create.vendor.vendor_type import get_or_create_vendor_type
from services.get_or_create.item_type import get_or_create_item_type
from services.get_or_create.vendor.vendor_item_type import get_or_create_vendor_item_type
from config import CLIENT_ID, CREATED_BY, CREATED_AT, CITY, STATE, STATE_ID, PROJECT_TYPE


city = CITY
state = STATE
state_id = STATE_ID


client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def load_vendors(conn):
    pairs = read_vendors_data()
    logger.info(f"Data read from Excel: {pairs}")

    item_type_keys = {}

    counters = {
        "vendor": {"created": 0, "existing": 0},
        "city": {"created": 0, "existing": 0},
        "state": {"created": 0, "existing": 0},
        "vendor_type": {"created": 0, "existing": 0},
        "item_type": {"created": 0, "existing": 0},
        "vendor_item_type": {"created": 0, "existing": 0}
    }

    for vendors_name, vendor_item_type, vendor_type in pairs:
        state_key, created = get_or_create_state(conn, state_id, state)
        if created:
            counters["state"]["created"] += 1
        else:
            counters["state"]["existing"] += 1
        logger.info(f"The key of the state '{state}' is: '{state_key}'")

        city_key, created = get_or_create_city(conn, city, state_key)
        if created:
            counters["city"]["created"] += 1
        else:
            counters["city"]["existing"] += 1
        logger.info(f"The key of the city '{city}' is: '{city_key}'")

        vendor_type_key, created = get_or_create_vendor_type(
            conn, vendor_type)
        if created:
            counters["vendor_type"]["created"] += 1
        else:
            counters["vendor_type"]["existing"] += 1
        logger.info(
            f"The key of the vendor type '{vendor_type}' is: '{vendor_type_key}'")

        vendor_key, created = get_or_create_vendor(
            conn, vendors_name, vendor_type_key, state_key, city_key
        )
        if created:
            counters["vendor"]["created"] += 1
        else:
            counters["vendor"]["existing"] += 1
        logger.info(
            f"The key of the vendor '{vendors_name}' is: '{vendor_key}'")

        item_type_keys[vendors_name] = []
        for item_type in vendor_item_type:
            item_type_key, created = get_or_create_item_type(
                conn, item_type
            )
            item_type_keys[vendors_name].append(item_type_key)
            if created:
                counters["item_type"]["created"] += 1
            else:
                counters["item_type"]["existing"] += 1
            logger.info(
                f"The key of the vendor '{item_type}' is: '{item_type_key}'")
        for item_type in item_type_keys[vendors_name]:
            vendor_item_type_key, created = get_or_create_vendor_item_type(
                conn, vendor_key, item_type
            )
            if created:
                counters["vendor_item_type"]["created"] += 1
            else:
                counters["vendor_item_type"]["existing"] += 1
            logger.info(
                f"The key of the vendor_item_type '{vendor_item_type}' is: '{vendor_item_type_key}'")

    conn.commit()
    logger.info("All operations completed successfully. Transaction committed.")

    for service, count in counters.items():
        logger.info(
            f"{service.capitalize()} - Created: {count['created']}, Existing: {count['existing']}"
        )

    return counters
