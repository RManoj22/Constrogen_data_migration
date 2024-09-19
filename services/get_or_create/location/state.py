import psycopg2
from utils.logger import logger
from queries.location.state import get_state, create_state

def get_or_create_state(conn, state_id, state_name):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve state: '{state_name}'")
            cursor.execute(get_state, (state_name,))
            result = cursor.fetchone()

            if result:
                state_key = result[0]
                logger.info(
                    f"State '{state_name}' found with key: '{state_key}'")
                return state_key, False
            else:
                logger.info(
                    f"State '{state_name}' not found, creating new entry.")
                cursor.execute(create_state, (state_id, state_name))
                state_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new state '{state_name}' with key: '{state_key}'")
                return state_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing state '{state_name}': {e}")
        raise
