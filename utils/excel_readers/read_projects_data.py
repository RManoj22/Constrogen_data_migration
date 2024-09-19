import pandas as pd
from utils.logger import logger
from ..validate_file import validate_file
from ..convert_values import convert_values
from config import PROJECTS_EXCEL_FILE_PATH

file_path = PROJECTS_EXCEL_FILE_PATH


def read_projects_data():
    try:
        validate_file(file_path)

        logger.info(f"Reading Excel file from path: {file_path}")
        df = pd.read_excel(file_path)

        if df.empty:
            logger.error("The Excel file is empty after reading")
            raise ValueError("The Excel file contains no data")

        logger.info("Excel file read successfully")

        required_columns = ["ProjectName",
                            "ProjectStatus", "NoofUnits", "ProjectAddress"]
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Excel file does not contain '{col}' column")
                raise ValueError(f"Excel file must contain '{col}' column")

        df['ProjectName'] = df['ProjectName'].apply(convert_values)
        df['ProjectStatus'] = df['ProjectStatus'].apply(convert_values)
        df['NoofUnits'] = df['NoofUnits'].apply(
            lambda x: x if pd.isna(x) else str(x).strip())
        df['ProjectAddress'] = df['ProjectAddress'].apply(convert_values)

        df = df[required_columns].to_records(index=False).tolist()
        logger.info(f"Processed {len(df)} project records")
        return df

    except Exception as e:
        logger.error(f"Error reading project data from Excel file: {e}")
        raise
