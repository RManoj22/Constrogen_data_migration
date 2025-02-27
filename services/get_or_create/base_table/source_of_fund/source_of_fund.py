import psycopg2
from utils.logger import logger
from queries.base_table.source_of_fund.source_of_fund import get_source_of_fund, create_source_of_fund


def get_or_create_source_of_fund(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve Source Of Fund: '{description}'")
            cursor.execute(get_source_of_fund, (description,))
            result = cursor.fetchone()

            if result:
                source_of_fund_key = result[0]
                logger.info(
                    f"Source Of Fund '{description}' found with Key: '{source_of_fund_key}'")
                return source_of_fund_key, False
            else:
                logger.info(
                    f"Source Of Fund '{description}' not found, creating new entry.")
                cursor.execute(create_source_of_fund, (description,))
                source_of_fund_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new source Of fund '{description}' with Key: '{source_of_fund_key}'")
                return source_of_fund_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing Source Of Fund '{description}': {e}")
        raise
