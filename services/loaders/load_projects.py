from utils.logger import logger
from utils.excel_readers.read_projects_data import read_projects_data
from services.get_or_create.location.city import get_or_create_city
from services.get_or_create.location.state import get_or_create_state
from services.get_or_create.project.project import get_or_create_project
from services.get_or_create.project.project_type import get_or_create_project_type
from services.get_or_create.project.project_status import get_or_create_project_status
from config import CLIENT_ID, CREATED_BY, CREATED_AT, CITY, STATE, STATE_ID, PROJECT_TYPE


city = CITY
state = STATE
state_id = STATE_ID
project_type = PROJECT_TYPE


client_id = CLIENT_ID
created_by = CREATED_BY
created_at = CREATED_AT


def load_projects(conn):
    projects = read_projects_data()
    logger.info(f"Data read from Excel: {projects}")

    counters = {
        "project": {"created": 0, "existing": 0},
        "city": {"created": 0, "existing": 0},
        "state": {"created": 0, "existing": 0},
        "project_type": {"created": 0, "existing": 0},
        "project_status": {"created": 0, "existing": 0}
    }


    for project_name, project_status, no_of_units, project_address in projects:
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

        project_type_key, created = get_or_create_project_type(
            conn, project_type)
        if created:
            counters["project_type"]["created"] += 1
        else:
            counters["project_type"]["existing"] += 1
        logger.info(
            f"The key of the project type '{project_type}' is: '{project_type_key}'")

        project_status_key, created = get_or_create_project_status(
            conn, project_status)
        if created:
            counters["project_status"]["created"] += 1
        else:
            counters["project_status"]["existing"] += 1
        logger.info(
            f"The key of the project type '{project_status}' is: '{project_status_key}'")


        project_key, created = get_or_create_project(
            conn, project_name, project_status_key, no_of_units, project_address, state_key, city_key, project_type_key)
        if created:
            counters["project"]["created"] += 1
        else:
            counters["project"]["existing"] += 1
        logger.info(
            f"The key of the project '{project_name}' is: '{project_key}'")

    conn.commit()
    logger.info("All operations completed successfully. Transaction committed.")

    for service, count in counters.items():
        logger.info(
            f"{service.capitalize()} - Created: {count['created']}, Existing: {count['existing']}"
        )

    return counters
