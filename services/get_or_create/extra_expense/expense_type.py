import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID
from queries.extra_expense.expense_type import get_expense_type, create_expense_type

client_id = CLIENT_ID
company_id = COMPANY_ID


def get_or_create_expense_type(conn, expense_type_description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve expense type with description: '{expense_type_description}' and company ID: '{company_id}'")
            cursor.execute(get_expense_type, (expense_type_description, company_id))
            result = cursor.fetchone()

            if result:
                expense_type_key = result[0]
                logger.info(
                    f"expense type '{expense_type_description}' found with key: '{expense_type_key}'")
                return expense_type_key, False
            else:
                logger.info(
                    f"expense type '{expense_type_description}' not found, creating new entry.")
                cursor.execute(create_expense_type, (expense_type_description, client_id, company_id))
                expense_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new expense type '{expense_type_description}' with key: '{expense_type_key}'")
                return expense_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing expense type '{expense_type_description}': {e}")
        raise
