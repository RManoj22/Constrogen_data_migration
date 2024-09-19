import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.location.city import get_city, create_city

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_city(conn, city_name, state_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve city with name: '{city_name}' and state key: '{state_key}'")
            cursor.execute(get_city, (city_name, company_id, state_key))
            result = cursor.fetchone()

            if result:
                city_key = result[0]
                logger.info(
                    f"City '{city_name}' found with key: '{city_key}'")
                return city_key, False
            else:
                logger.info(
                    f"City '{city_name}' not found, creating new entry.")
                cursor.execute(create_city, (city_name, created_by, created_at,
                               client_id, company_id, state_key))
                city_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new city '{city_name}' with key: '{city_key}'")
                return city_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing city '{city_name}': {e}")
        raise
