import pandas as pd
from utils.logger import logger

def convert_values(value_str):
    try:
        if pd.isna(value_str):
            return None

        return value_str.strip().title()

    except Exception as e:
        logger.error(f"Error parsing value: {e}")
        raise ValueError("Error parsing value") from e