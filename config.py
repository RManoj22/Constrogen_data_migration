import os
from datetime import datetime

current_directory = os.getcwd()

CLIENT_ID = 1
COMPANY_ID = 1
CREATED_BY = 'admin'
CREATED_AT = datetime.now()

# Defaul vendor
DEFAULT_VENDOR_KEY = 73

# Defaul item
DEFAULT_ITEM_KEY = 1124

# Location
CITY = 'Chennai'
STATE = 'Tamil Nadu'
STATE_ID = 'TN'

# Project
PROJECT_FILE_NAME = 'Projects.xlsx'
PROJECTS_EXCEL_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\projects\Projects.xlsx'
PROJECT_CODE_COUNTER = 1
PROJECT_TYPE = 'Construction'
PROJECT_CODE = f"2024_{PROJECT_CODE_COUNTER}"
LOAD_PROJECTS = False
# LOAD_PROJECTS = True

# Vendor
VENDORS_FILE_NAME = 'Vendors.xlsx'
VENDORS_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\vendors\Vendors.xlsx'
LOAD_VENDORS = False
# LOAD_VENDORS = True

# Items
ITEMS_FILE_NAME = 'Items.xlsx'
ITEMS_EXCEL_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\items\Items.xlsx'
LOAD_ITEMS = False
# LOAD_ITEMS = True

# Vendor purchase order and items
BILLS_FILE_NAME = 'filtered_bill_header.xlsx'
BILLS_EXCEL_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\bills\placid\placid bill header.xlsx'
SECOND_EXCEL_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\bills\placid\Perfect Placid Stock Record.xlsx'
GUI_OUTPUT_FILE_PATH = r'D:\IGS\Constrogen_data_migration\files\bills\gui_output\output_file.xlsx'
# LOAD_BILLS = False
LOAD_BILLS = True
