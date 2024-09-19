import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values
from config import VENDORS_FILE_PATH

file_path = VENDORS_FILE_PATH


def read_vendors_data():
    try:
        validate_file(file_path)

        logger.info(f"Reading Excel file from path: {file_path}")
        df = pd.read_excel(file_path)

        required_columns = ["ItemVendorName", "ItemTypeList",
                            "ItemVendorType"]
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        def process_item_types(item_type, row_index):
            try:
                return [item.strip().title() for item in item_type.split(',')]
            except Exception as split_error:
                logger.error(
                    f"Error processing item_type column at row {row_index}: {split_error}")
                raise ValueError(
                    f"There was an issue processing the item_type column at row {row_index}") from split_error
        df['ItemTypeList'] = df.apply(lambda row: process_item_types(
            row['ItemTypeList'], row.name), axis=1)
        df['ItemVendorName'] = df['ItemVendorName'].apply(convert_values)
        df['ItemVendorType'] = df['ItemVendorType'].apply(convert_values)
        pairs = list(zip(df['ItemVendorName'],
                     df['ItemTypeList'], df['ItemVendorType']))
        return pairs

    except Exception as e:
        logger.error(f"Error reading vendors data from Excel file: {e}")
        raise
