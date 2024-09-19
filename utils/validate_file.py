import os
from utils.logger import logger


def validate_file(file_path):

    if not os.path.exists(file_path):
        logger.error(f"File not found at path: {file_path}")
        raise FileNotFoundError(
            f"The file does not exist at the specified path: {file_path}")

    if os.path.getsize(file_path) == 0:
        logger.error(f"The file at path {file_path} is empty")
        raise ValueError("The file is empty")

    logger.info(f"File at path {file_path} is valid")
