from utils.logger import logger
from utils.excel_readers.read_contractors_data import read_contractors_data
# from services.get_or_create.location.city import get_or_create_city
# from services.get_or_create.location.state import get_or_create_state
from services.get_or_create.contractor.contractor_type import get_or_create_contractor_type
from services.get_or_create.contractor.contractor import get_or_create_contractor
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def load_contractors(conn):
    contractors = read_contractors_data()
    logger.info(f"Data read from Excel: {contractors}")

    counters = {
        "contractor": {"created": 0, "existing": 0},
        "city": {"created": 0, "existing": 0},
        "state": {"created": 0, "existing": 0},
        "contractor_type": {"created": 0, "existing": 0}
    }

    for contractor_name, work_type, inhouse_value in contractors:
        # # Fetch or create the state
        # state_key, created = get_or_create_state(conn, contractor_name)
        # if created:
        #     counters["state"]["created"] += 1
        # else:
        #     counters["state"]["existing"] += 1
        # logger.info(f"The key of the state is: '{state_key}'")

        # # Fetch or create the city
        # city_key, created = get_or_create_city(conn, contractor_name, state_key)
        # if created:
        #     counters["city"]["created"] += 1
        # else:
        #     counters["city"]["existing"] += 1
        # logger.info(f"The key of the city is: '{city_key}'")

        # Fetch or create contractor type (based on 'WorkType')
        contractor_type_key, created = get_or_create_contractor_type(
            conn, work_type)
        if created:
            counters["contractor_type"]["created"] += 1
        else:
            counters["contractor_type"]["existing"] += 1
        logger.info(
            f"The key of the contractor type '{work_type}' is: '{contractor_type_key}'")

        # Fetch or create contractor
        contractor_key, created = get_or_create_contractor(
            conn,
            contractor_name,
            # city_key,
            # state_key,
            client_id,
            company_id,
            contractor_type_key,
            created_by,
            created_at,
            inhouse_value
        )
        if created:
            counters["contractor"]["created"] += 1
        else:
            counters["contractor"]["existing"] += 1
        logger.info(
            f"The key of the contractor '{contractor_name}' is: '{contractor_key}'")

    conn.commit()
    logger.info("All operations completed successfully. Transaction committed.")

    # Log the number of records created vs existing
    for service, count in counters.items():
        logger.info(
            f"{service.capitalize()} - Created: {count['created']}, Existing: {count['existing']}"
        )

    return counters
