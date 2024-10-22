import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.mode_of_pay.mode_of_pay import get_mode_of_pay_query, create_mode_of_pay_query

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_next_mode_of_pay_key(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COALESCE(MAX("ModeOfPay")::int, 0) 
                FROM "ModeOfPay";
            """)
            result = cursor.fetchone()[0]
            next_key = str(result + 1)
            return next_key
    except psycopg2.Error as e:
        logger.error(
            f"Database error while retrieving the next ModeOfPay key: {e}")
        raise


def get_or_create_mode_of_pay(conn, mode_of_pay_descr):
    try:
        with conn.cursor() as cursor:
            mode_of_pay = get_next_mode_of_pay_key(conn)

            logger.info(
                f"Attempting to retrieve mode of pay: '{mode_of_pay_descr}'")
            cursor.execute(get_mode_of_pay_query, (mode_of_pay_descr,))
            result = cursor.fetchone()

            if result:
                mode_of_pay_key = result[0]
                logger.info(
                    f"Mode of pay '{mode_of_pay_descr}' found with key {mode_of_pay_key}")
                return mode_of_pay_key, False
            else:
                logger.info(
                    f"Mode of pay '{mode_of_pay_descr}' not found, creating new entry.")
                cursor.execute(create_mode_of_pay_query,
                               (mode_of_pay, mode_of_pay_descr))
                mode_of_pay_key = cursor.fetchone()[0]
                logger.info(
                    f"Mode of pay '{mode_of_pay_descr}' created with key {mode_of_pay_key}")
                return mode_of_pay, True
    except psycopg2.Error as e:
        logger.error(f"Database error while processing mode of pay: {e}")
        raise
