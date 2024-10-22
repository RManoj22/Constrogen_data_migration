import psycopg2
from utils.logger import logger


def get_last_number(conn, query, company_id, client_id):
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (company_id, client_id))
            result = cursor.fetchone()
            # Start from 1000 to increment to 1001 later
            return int(result[0]) if result else 1000
    except psycopg2.Error as e:
        logger.error(
            f"Error fetching the last number for the query {query}: {e}")
        raise
