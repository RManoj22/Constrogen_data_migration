import psycopg2
import pandas as pd
from utils.logger import logger
from queries.item.item import get_item_with_descr
from config import GUI_OUTPUT_FILE_PATH, DEFAULT_ITEM_KEY

default_item_key = DEFAULT_ITEM_KEY
gui_output_file_path = GUI_OUTPUT_FILE_PATH


class ItemNotFoundError(Exception):
    """Custom exception raised when an item is not found in the database."""

    def __init__(self, item_name):
        self.item_name = item_name
        super().__init__(f"Item '{self.item_name}' not found in the database.")


def get_or_set_default_item(conn, item_name, default_item_list):
    # Read the Excel file (specify the correct file path)
    excel_file = gui_output_file_path
    if default_item_list is None:
        default_item_list = []

    try:
        df = pd.read_excel(excel_file)

        # Search for the item_name in the 'Current Item Name' column
        matched_row = df[df['Current Item Name'].str.strip(
        ).str.title() == item_name.strip().title()]

        if not matched_row.empty:
            # Get the 'Matched description' value from the matched row
            matched_description = matched_row.iloc[0]['Matched description']
            logger.info(
                f"Matched description for item '{item_name}': {matched_description}")

            try:
                with conn.cursor() as cursor:
                    logger.info(
                        f"Attempting to retrieve item key from the db: '{matched_description}'")

                    cursor.execute(get_item_with_descr, (matched_description,))
                    result = cursor.fetchone()

                    if result:
                        item_key = result[0]
                        logger.info(
                            f"Item: '{matched_description}' found with key: '{item_key}'")
                        return item_key
                    else:
                        # Log and raise custom exception if item not found in the database
                        logger.error(
                            f"Item '{matched_description}' not found in the database.")
                        raise ItemNotFoundError(item_name)

            except psycopg2.Error as e:
                logger.error(
                    f"Database error while trying to find item key of '{matched_description}': {e}")
                raise  # re-raise to stop the loop and propagate the error

        else:
            logger.info(
                f"No match found for item '{item_name}' in the Excel file. Returning default item key")
            default_item_list.append(item_name)
            return default_item_key

    except FileNotFoundError:
        logger.error(f"Excel file not found: {excel_file}")
    except ItemNotFoundError as e:
        # Log the custom exception message and stop the loop
        logger.error(f"Item not found error: {e}")
        raise  # re-raise to stop the loop and propagate the error
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise  # re-raise to stop the loop and propagate the error
