import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values, strip_spaces
from config import CONTRACTOR_PAYMENTS_EXCEL_FILE_PATH

file_path = CONTRACTOR_PAYMENTS_EXCEL_FILE_PATH


def read_contractor_payments_data():
    try:
        # Validate the file
        validate_file(file_path)

        logger.info(f"Reading Excel file from path: {file_path}")
        df = pd.read_excel(file_path)
        logger.info("Excel file read successfully")
        # Log a preview of the file's data
        logger.info(f"Data from file: {df.head()}")

        # Validate required columns
        required_columns = ['DateCreated', 'ProjectName',
                            'VendorName', 'BillAmount']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        # Clean and process the file
        df['VendorName'] = df['VendorName'].apply(convert_values)
        df['ProjectName'] = df['ProjectName'].apply(convert_values)
        df['BillAmount'] = df['BillAmount'].apply(strip_spaces).astype(float)
        df['DateCreated'] = pd.to_datetime(df['DateCreated']).dt.date  # Convert to datetime

        # Convert the DataFrame rows to a list of tuples and return
        data_tuples = [tuple(row) for row in df[['DateCreated', 'ProjectName',
                                                 'VendorName', 'BillAmount']].to_records(index=False)]
        # Log the first 5 rows of data to be returned
        logger.info(f"Data to be returned: {data_tuples[:5]}")

        return data_tuples

    except Exception as e:
        logger.error(f"Error processing Excel file: {e}")
        raise
