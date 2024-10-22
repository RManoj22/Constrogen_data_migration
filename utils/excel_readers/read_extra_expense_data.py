import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values, strip_spaces
from config import EXPENSES_HEADER_EXCEL_FILE_PATH, EXPENSES_DETAIL_EXCEL_FILE_PATH


file_path = EXPENSES_HEADER_EXCEL_FILE_PATH
second_file_path = EXPENSES_DETAIL_EXCEL_FILE_PATH

def read_extra_expense_data():
    try:
        # Validate both files
        validate_file(file_path)
        validate_file(second_file_path)

        logger.info(f"Reading Excel file from path: {file_path}")
        df_first = pd.read_excel(file_path)
        logger.info("First Excel file read successfully")
        logger.info(f"Data from first file: {df_first.head()}")  # Log a preview of the first file's data

        # Validate required columns in the first file
        required_columns_first = ['BillNo', 'DateCreated', 'MaterialType',
                                  'VendorName', 'BillAmount', 'ProjectName']
        for col in required_columns_first:
            if col not in df_first.columns:
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        # Clean and process first file
        df_first['BillNo'] = df_first['BillNo'].apply(strip_spaces).astype('Int64')
        df_first['DateCreated'] = df_first['DateCreated'].apply(strip_spaces)
        df_first['DateCreated'] = pd.to_datetime(df_first['DateCreated']).dt.date
        df_first['MaterialType'] = df_first['MaterialType'].apply(convert_values)
        df_first['VendorName'] = df_first['VendorName'].apply(convert_values)
        df_first['ProjectName'] = df_first['ProjectName'].apply(convert_values)

        # Read the second Excel file
        logger.info(f"Reading second Excel file from path: {second_file_path}")
        df_second = pd.read_excel(second_file_path)
        logger.info("Second Excel file read successfully")
        logger.info(f"Data from second file: {df_second.head()}")  # Log a preview of the second file's data

        # Validate required columns in the second file
        required_columns_second = ['BillNO', 'ItemName']
        for col in required_columns_second:
            if col not in df_second.columns:
                logger.error(f"Second Excel file does not contain '{col}' column")
                raise ValueError(f"Second Excel file must contain '{col}' column")

        # Clean and process second file
        df_second['BillNO'] = df_second['BillNO'].apply(strip_spaces).astype('Int64')
        df_second['ItemName'] = df_second['ItemName'].apply(convert_values)  # Apply convert_values to ItemName

        # Merge the two DataFrames based on 'BillNo' and 'BillNO'
        merged_df = pd.merge(df_first, df_second, how='inner', left_on='BillNo', right_on='BillNO')
        logger.info(f"Merged DataFrame: {merged_df.head()}")  # Log a preview of the merged data

        # Select required columns, including MaterialType
        result = merged_df[['DateCreated', 'BillNo', 'MaterialType', 'VendorName', 'BillAmount', 'ProjectName', 'ItemName']]

        # Convert the DataFrame rows to a list of tuples and return
        data_tuples = [tuple(row) for row in result.to_records(index=False)]
        logger.info(f"Data to be returned: {data_tuples[:5]}")  # Log the first 5 rows of data to be returned

        return data_tuples

    except Exception as e:
        logger.error(f"Error processing Excel files: {e}")
        raise
