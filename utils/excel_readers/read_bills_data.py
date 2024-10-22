import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values, strip_spaces
from config import BILLS_EXCEL_FILE_PATH, SECOND_EXCEL_FILE_PATH

file_path = BILLS_EXCEL_FILE_PATH
second_file_path = SECOND_EXCEL_FILE_PATH


def calculate_gst_and_net_amount(bill_amount, final_bill_amount):
    """Calculate GST and net amount based on BillAmount and FinalBillAmount."""
    if pd.isna(final_bill_amount):
        # If no FinalBillAmount, return BillAmount as net amount and GST as 0
        return bill_amount, 0.0
    else:
        # Assuming GST is the difference between BillAmount and FinalBillAmount
        gst_amount = final_bill_amount - bill_amount
        return final_bill_amount, gst_amount


def read_bills_data():
    try:
        validate_file(file_path)
        validate_file(second_file_path)  # Validate the second file as well

        logger.info(f"Reading Excel file from path: {file_path}")
        df = pd.read_excel(file_path)

        logger.info("First Excel file read successfully")

        # Validate required columns in the first file
        required_columns = ['BillNo', 'DateCreated', 'MaterialType',
                            'VendorName', 'BillAmount', 'FinalBillAmount', 'ProjectName']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        # Apply strip_spaces to numeric columns and convert back to int/float
        df['BillNo'] = df['BillNo'].apply(strip_spaces).astype('Int64')
        df['DateCreated'] = df['DateCreated'].apply(strip_spaces)

        # Convert 'DateCreated' to date only format (remove time part)
        df['DateCreated'] = pd.to_datetime(df['DateCreated']).dt.date

        df['BillAmount'] = df['BillAmount'].apply(strip_spaces).astype(float)
        df['FinalBillAmount'] = df['FinalBillAmount'].apply(
            strip_spaces).astype(float)

        # Apply convert_values to string columns
        df['MaterialType'] = df['MaterialType'].apply(convert_values)
        df['VendorName'] = df['VendorName'].apply(convert_values)
        df['ProjectName'] = df['ProjectName'].apply(convert_values)

        # Calculate GST and net amounts for each row
        df[['NetAmount', 'GSTAmount']] = df.apply(
            lambda row: pd.Series(calculate_gst_and_net_amount(
                row['BillAmount'], row['FinalBillAmount'])),
            axis=1
        )

        # Round the NetAmount and GSTAmount to 2 decimal places
        df['NetAmount'] = df['NetAmount'].round(2)
        df['GSTAmount'] = df['GSTAmount'].round(2)

        # Read the second Excel file
        logger.info(f"Reading second Excel file from path: {second_file_path}")
        df_second = pd.read_excel(second_file_path)

        logger.info("Second Excel file read successfully")

        # Validate that the second file contains the 'BillNo' column
        if 'BillNo' not in df_second.columns:
            logger.error("Second Excel file must contain 'BillNo' column")
            raise ValueError("Second Excel file must contain 'BillNo' column")

        # Strip spaces in the second file and ensure BillNo is consistent
        df_second['BillNo'] = df_second['BillNo'].apply(
            strip_spaces).astype('Int64')

        # Ensure both 'ItemPrice' and 'ItemQuantity' are numeric before rounding
        df_second['ItemPrice'] = pd.to_numeric(df_second['ItemPrice'], errors='coerce').round(2)
        df_second['ItemQuantity'] = pd.to_numeric(df_second['ItemQuantity'], errors='coerce').round(2)

        # Group the second file data by BillNo
        grouped_data = df_second.groupby('BillNo').apply(
            lambda x: x.to_dict(orient='records')).to_dict()

        # Create the final list of tuples with matching rows from the second file
        pairs = []
        for _, row in df.iterrows():
            bill_no = row['BillNo']
            # Fetch matching rows or empty list if no matches
            matching_rows = grouped_data.get(bill_no, [])

            pairs.append((
                row['BillNo'],
                row['DateCreated'],
                row['MaterialType'],
                row['VendorName'],
                row['NetAmount'],
                row['GSTAmount'],
                row['ProjectName'],
                matching_rows  # Append the list of matching rows from the second file
            ))

        return pairs

    except Exception as e:
        logger.error(f"Error reading Excel files: {e}")
        raise
