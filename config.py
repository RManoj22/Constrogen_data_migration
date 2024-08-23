from datetime import datetime
import os

CLIENT_ID = 1
CREATED_BY = 'admin'
CREATED_AT = datetime.now()

current_directory = os.getcwd()

file_name = 'new_items.xlsx'

EXCEL_FILE_PATH = os.path.join(current_directory, file_name)
