from utils.logger import logger
from utils.excel_readers.read_base_table_data import read_base_table_data
from services.get_or_create.location.city import get_or_create_city
from services.get_or_create.location.state import get_or_create_state
from services.get_or_create.base_table.client.client import get_or_create_client
from services.get_or_create.base_table.company.company import get_or_create_company
from services.get_or_create.base_table.mode_of_pay.mode_of_pay import get_or_create_mode_of_pay
from services.get_or_create.base_table.source_of_fund.source_of_fund import get_or_create_source_of_fund


def load_base_table(conn):
    states_data, cities_data, clients_data, companies_data, mode_of_pay_data, source_of_fund_data = read_base_table_data()

    logger.info("Starting data loading process...")

    counters = {
        "state": {"created": 0, "existing": 0},
        "city": {"created": 0, "existing": 0},
        "client": {"created": 0, "existing": 0},
        "company": {"created": 0, "existing": 0},
        "modeofpay": {"created": 0, "existing": 0},
        "source_of_fund": {"created": 0, "existing": 0}
    }

    for state_id, state_name in states_data:
        state_key, created = get_or_create_state(conn, state_id, state_name)
        counters["state"]["created" if created else "existing"] += 1

    for city_name, state_name in cities_data:
        state_key, _ = get_or_create_state(conn, None, state_name)
        city_key, created = get_or_create_city(conn, city_name, state_key)
        counters["city"]["created" if created else "existing"] += 1

    for client_name in clients_data:
        client_key, created = get_or_create_client(conn, client_name)
        counters["client"]["created" if created else "existing"] += 1

    for company_name, client_name in companies_data:
        client_key, _ = get_or_create_client(conn, client_name)
        company_key, created = get_or_create_company(
            conn, company_name, client_key)
        counters["company"]["created" if created else "existing"] += 1

    for mode_of_pay_id, description in mode_of_pay_data:
        _, created = get_or_create_mode_of_pay(
            conn, description, mode_of_pay_id)
        counters["modeofpay"]["created" if created else "existing"] += 1

    for source_of_fund_desc in source_of_fund_data:
        _, created = get_or_create_source_of_fund(conn, source_of_fund_desc)
        counters["source_of_fund"]["created" if created else "existing"] += 1

    conn.commit()
    logger.info("All data loaded successfully.")

    return counters
