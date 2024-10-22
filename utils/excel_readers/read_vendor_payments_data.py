import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from config import PAYMENT_EXCEL_FILE_PATH


file_path = PAYMENT_EXCEL_FILE_PATH


def read_vendor_payments_data():
    try:
        validate_file(file_path)
        logger.info(f"Reading Excel file from path: {file_path}")

        df = pd.read_excel(file_path)
        logger.info("Payment data file read successfully")

        combined_data = [
            {'BillNo': row['BillNo'], 'PaymentMode': row['PaymentMode']}
            for index, row in df.iterrows()
        ]

        logger.info(
            "Payment data file read successfully, returning combined data")
        return combined_data

    except Exception as e:
        logger.error(f"Error reading Excel files: {e}")
        raise
