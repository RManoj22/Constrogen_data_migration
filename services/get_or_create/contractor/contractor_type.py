import psycopg2
from utils.logger import logger
from config import CLIENT_ID, COMPANY_ID, CREATED_BY, CREATED_AT
from queries.contractor.contractor_type import get_contractor_type, create_contractor_type

client_id = CLIENT_ID
company_id = COMPANY_ID
created_by = CREATED_BY
created_at = CREATED_AT


def get_or_create_contractor_type(conn, description):
    try:
        with conn.cursor() as cursor:
            logger.info(
                f"Attempting to retrieve contractor type: '{description}' with client id {client_id} and company id {company_id}"
            )
            cursor.execute(get_contractor_type,
                           (description, client_id, company_id))
            result = cursor.fetchone()

            if result:
                contractor_type_key = result[0]
                logger.info(
                    f"Contractor type '{description}' with client id {client_id} and company id {company_id}, found with key: '{contractor_type_key}'"
                )
                return contractor_type_key, False
            else:
                logger.info(
                    f"Contractor type '{description}' with client id {client_id} and company id {company_id} not found, creating new entry."
                )
                cursor.execute(create_contractor_type, (description, created_by,
                               created_at, client_id, company_id))
                contractor_type_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new contractor type '{description}' where client id {client_id} and company id {company_id},  with key: '{contractor_type_key}'"
                )
                return contractor_type_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing contractor type '{description}' with client id {client_id} and company id {company_id}: {e}"
        )
        raise
