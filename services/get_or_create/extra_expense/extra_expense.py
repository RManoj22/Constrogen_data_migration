import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID
from queries.extra_expense.extra_expense import get_extra_expense, create_extra_expense

client_id = CLIENT_ID
company_id = COMPANY_ID


def get_or_create_extra_expense(conn, date, amount, payment_desc, mode_of_pay_key, project_key, expense_type_key):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve extra expense with date {date}, amount {amount}, project_key {project_key} and expense_type_key {expense_type_key}")
            cursor.execute(get_extra_expense, (date, amount, expense_type_key, project_key))
            result = cursor.fetchone()

            if result:
                extra_expense_key = result[0]
                logger.info(
                    f"extra expense with date {date}, amount {amount}, project_key {project_key} and expense_type_key {expense_type_key} found with key: '{extra_expense_key}'")
                return extra_expense_key, False
            else:
                logger.info(
                    f"extra expense with date {date}, amount {amount}, project_key {project_key} and expense_type_key {expense_type_key} not found, creating new entry.")
                cursor.execute(create_extra_expense, (date, amount, payment_desc, client_id, company_id, mode_of_pay_key, project_key, expense_type_key))
                extra_expense_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new extra expense where date {date}, amount {amount}, project_key {project_key} and expense_type_key {expense_type_key} with key: '{extra_expense_key}'")
                return extra_expense_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing extra expense with date {date}, amount {amount}, project_key {project_key} and expense_type_key {expense_type_key}: {e}")
        raise
