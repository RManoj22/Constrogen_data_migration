import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from config import BASE_TABLE_DATA_EXCEL_FILE_PATH

file_path = BASE_TABLE_DATA_EXCEL_FILE_PATH

REQUIRED_SHEETS = {
    "States": ["State_ID", "State_Name"],
    "Cities": ["City_Name", "City_State_Name"],
    "Clients": ["Client_Name"],
    "Companies": ["Company_Name", "Company_Client_Name"],
    "Mode of Pay": ["ModeOfPay", "ModeOfPay_Descr"],
    "Source of Fund": ["SourceOfFund_Name"]
}


def read_base_table_data():
    try:
        xl = pd.ExcelFile(file_path)
        available_sheets = xl.sheet_names

        missing_sheets = [sheet for sheet in REQUIRED_SHEETS if sheet not in available_sheets]
        if missing_sheets:
            logger.error(f"Missing sheets in the Excel file: {missing_sheets}")
            raise ValueError(f"Missing sheets: {missing_sheets}")

        validate_file(file_path)

        extracted_data = {}

        for sheet_name, expected_columns in REQUIRED_SHEETS.items():
            df = xl.parse(sheet_name)
            missing_columns = [col for col in expected_columns if col not in df.columns]

            if missing_columns:
                logger.error(f"Missing columns in '{sheet_name}' sheet: {missing_columns}")
                raise ValueError(f"Missing columns in '{sheet_name}': {missing_columns}")

            extracted_data[sheet_name] = df[expected_columns].dropna().to_records(index=False).tolist()

        return (
            extracted_data["States"],
            extracted_data["Cities"],
            extracted_data["Clients"],
            extracted_data["Companies"],
            extracted_data["Mode of Pay"],
            extracted_data["Source of Fund"],
        )

    except Exception as e:
        logger.error(f"Error reading Excel data: {e}")
        raise
