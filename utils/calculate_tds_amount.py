import numpy as np
from utils.logger import logger


def calculate_tds_amount(amount):
    if amount is None or not isinstance(amount, (int, float, np.float64, np.int64)):
        logger.error(
            f"Error while calculating TDS amount for the value {amount}. Provide a valid amount!")
        raise TypeError(
            f"Invalid amount type. Must be an int or float. The value provided is an {type(amount)}")
    else:
        tds_amount = amount * 1 / 100
        logger.info(f"TDS amount for the value {amount} is {tds_amount}")
        return tds_amount
