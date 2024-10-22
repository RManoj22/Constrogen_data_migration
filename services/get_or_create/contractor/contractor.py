import psycopg2
from utils.logger import logger
from queries.contractor.contractor import get_simple_contractor, get_contractor, create_contractor


def get_or_create_contractor(conn, contractor_name, client_id, company_id, contractor_type_key=None, created_by=None, created_at=None, inhouse_value=None, city_key=None, state_key=None, **kwargs):

    try:
        with conn.cursor() as cursor:
            if contractor_type_key is None:
                logger.info(
                    f"Attempting to retrieve contractor (simple query): '{contractor_name}' with client id {client_id} and company id {company_id}"
                )
                cursor.execute(get_simple_contractor,
                               (contractor_name, client_id, company_id))
                result = cursor.fetchone()

                if result:
                    contractor_key = result[0]
                    logger.info(
                        f"Contractor (simple query) '{contractor_name}' with client id {client_id} and company id {company_id} found with key: '{contractor_key}'"
                    )
                    return contractor_key, False
            logger.info(
                f"Attempting to retrieve contractor: '{contractor_name}' with contractor_type_key {contractor_type_key}, client id {client_id} and company id {company_id}"
            )
            cursor.execute(get_contractor, (contractor_name,
                           contractor_type_key, client_id, company_id))
            result = cursor.fetchone()

            if result:
                contractor_key = result[0]
                logger.info(
                    f"Contractor '{contractor_name}' with contractor_type_key {contractor_type_key}, client id {client_id} and company id {company_id}, found with key: '{contractor_key}'"
                )
                return contractor_key, False
            else:
                logger.info(
                    f"Contractor '{contractor_name}' with contractor_type_key {contractor_type_key}, client id {client_id} and company id {company_id} not found, creating new entry."
                )
                cursor.execute(create_contractor, (
                    contractor_name,
                    # kwargs.get('address1'),
                    # kwargs.get('address2'),
                    # kwargs.get('pincode'),
                    # kwargs.get('gst_number'),
                    # kwargs.get('contact_phone_no'),
                    # kwargs.get('contact_landline_no'),
                    # kwargs.get('contact_email'),
                    # kwargs.get('inactive'),
                    # kwargs.get('inhouse'),
                    created_by,
                    created_at,
                    # city_key,
                    client_id,
                    company_id,
                    contractor_type_key,
                    "N",
                    inhouse_value
                    # state_key
                ))
                contractor_key = cursor.fetchone()[0]
                logger.info(
                    f"Created new contractor '{contractor_name}' where contractor_type_key {contractor_type_key}, client id {client_id} and company id {company_id}, with key: '{contractor_key}'"
                )
                return contractor_key, True

    except psycopg2.Error as e:
        logger.error(
            f"Database error while processing contractor '{contractor_name}' with contractor_type_key {contractor_type_key}, client id {client_id} and company id {company_id}: {e}"
        )
        raise
