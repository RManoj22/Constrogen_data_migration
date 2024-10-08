import numpy as np
import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values
from config import ITEMS_EXCEL_FILE_PATH

file_path = ITEMS_EXCEL_FILE_PATH


def parse_spec_param(spec_param_str):
    try:
        if pd.isna(spec_param_str):
            return None

        if ',' in spec_param_str:
            pairs = [pair.split('=') for pair in spec_param_str.split(',')]
            spec_param_dict = {key.strip().title(): value.strip().title()
                               for key, value in pairs}
        else:
            key_value = spec_param_str.split('=')
            if len(key_value) == 2:
                spec_param_dict = {key_value[0].strip(
                ).title(): key_value[1].strip().title()}
            else:
                logger.error(
                    f"Incorrect format for 'Item sub type spec param': {spec_param_str}")
                raise ValueError(
                    "Incorrect format for 'Item sub type spec param'")

        return spec_param_dict

    except Exception as e:
        logger.error(f"Error parsing 'Item sub type spec param': {e}")
        raise ValueError("Error parsing 'Item sub type spec param'") from e


def read_items_data():
    try:
        validate_file(file_path)

        logger.info(f"Reading Excel file from path: {file_path}")
        df = pd.read_excel(file_path)

        logger.info("Excel file read successfully")

        required_columns = ['Item type', 'Item sub type', 'Item description',
                            'Purpose', 'UOM', 'Item sub type GST', 'Item sub type spec param']
        for col in required_columns:
            if (col not in df.columns):
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        df['Item type'] = df['Item type'].apply(convert_values)
        df['Item sub type'] = df['Item sub type'].apply(convert_values)
        df['Purpose'] = df['Purpose'].apply(convert_values)
        df['Item sub type GST'] = df['Item sub type GST'].fillna(0)
        df['Item description'] = df['Item description'].apply(convert_values)

        def process_uom(uom_str, row_index):
            try:
                return [item.strip().title() for item in uom_str.split(',')]
            except Exception as split_error:
                logger.error(
                    f"Error processing 'UOM' column at row {row_index}: {split_error}")
                raise ValueError(
                    f"There was an issue processing the 'UOM' column at row {row_index}") from split_error

        df['UOM'] = df.apply(lambda row: process_uom(
            row['UOM'], row.name), axis=1)

        def process_spec_param(spec_param_str, row_index):
            try:
                return parse_spec_param(spec_param_str)
            except Exception as parse_error:
                logger.error(
                    f"Error parsing 'Item sub type spec param' at row {row_index}: {parse_error}")
                raise ValueError(
                    f"Error parsing 'Item sub type spec param' at row {row_index}") from parse_error
        df['Item sub type spec param'] = df.apply(lambda row: process_spec_param(
            row['Item sub type spec param'], row.name), axis=1)

        pairs = list(zip(df['Item type'], df['Item sub type'], df['Item description'],
                         df['Purpose'], df['UOM'], df['Item sub type GST'], df['Item sub type spec param']))

        logger.info(f"Extracted {len(pairs)} pairs from Excel file")
        return pairs

    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        raise
