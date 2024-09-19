import os
from datetime import datetime

current_directory = os.getcwd()

CLIENT_ID = 1
COMPANY_ID = 1
CREATED_BY = 'admin'
CREATED_AT = datetime.now()

# Location
CITY = 'Chennai'
STATE = 'Tamil Nadu'
STATE_ID = 'TN'

# Project
PROJECT_FILE_NAME = 'Projects.xlsx'
PROJECTS_EXCEL_FILE_PATH = os.path.join(current_directory, PROJECT_FILE_NAME)
PROJECT_CODE_COUNTER = 1
PROJECT_TYPE = 'Construction'
PROJECT_CODE = f"2024_{PROJECT_CODE_COUNTER}"
LOAD_PROJECTS = False
# LOAD_PROJECTS = True

# Vendor
VENDORS_FILE_NAME = 'Vendors.xlsx'
VENDORS_FILE_PATH = os.path.join(current_directory, VENDORS_FILE_NAME)
LOAD_VENDORS = False
# LOAD_VENDORS = True

# Items
ITEMS_FILE_NAME = 'Items.xlsx'
ITEMS_EXCEL_FILE_PATH = os.path.join(current_directory, ITEMS_FILE_NAME)
LOAD_ITEMS = True
# LOAD_ITEMS = False
