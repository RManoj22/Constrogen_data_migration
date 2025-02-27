import psycopg2
from utils.logger import logger
from queries.base_table.mode_of_pay.mode_of_pay import get_mode_of_pay, create_mode_of_pay


def get_or_create_mode_of_pay(conn, description, mode_of_pay_id):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve mode of pay: '{description}'")
            cursor.execute(get_mode_of_pay, (description,))
            result = cursor.fetchone()

            if result:
                mode_of_pay_id = result[0]
                logger.info(
                    f"Mode of pay: '{description}' found with ID: '{mode_of_pay_id}'")
                return mode_of_pay_id, False
            else:
                logger.info(
                    f"Mode of pay: '{description}' not found, creating new entry.")
                cursor.execute(create_mode_of_pay,
                               (mode_of_pay_id, description))
                mode_of_pay_id = cursor.fetchone()[0]
                logger.info(
                    f"Created new mode of pay: '{description}' with ID: '{mode_of_pay_id}'")
                return mode_of_pay_id, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Mode of pay: '{description}': {e}")
        raise
