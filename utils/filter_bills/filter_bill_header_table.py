import pandas as pd

# File paths
# Replace with your input file name
input_file = r'D:\IGS\Constrogen_data_migration\files\bills\all_bills\all_bills_base_data.xlsx'
output_file = r'D:\IGS\Constrogen_data_migration\files\bills\filtered_bills\filtered_expenses_placid.xlsx'
# Load the data into a DataFrame
# Adjust the sheet name if necessary
df = pd.read_excel(input_file)

# List of values to include from the 'MaterialType' column
# Replace with the values you want to include


# Material types for creating purchase order
# include_material_types = ['Advertisement','Auditing Payment','Blue Metal','Bore','Brick','Cement','Concrete','Carpenter','Electrical','Elevation Colours','GraniteAndMarble','Grill','Painting','Plumbing','Sand','Steel','Tiles','UPVC Window','Water Proofing','Wood']

# Material types for creating extra expenses
include_material_types = [
'EB',
'Extra Expense',
'Flat Maintainence',
'Petrol Expense',
'Printer Toner Refill',
'Stationary',
'System Purchase and Repair',
'Water Supply',
'Interest Payment',
'Electronics',
# 'Interior Work',
'Plan Approval',
'Property Tax',
'Rent',
'Salary and Allowance'
]

# List of project names to include in the 'ProjectName' column
# Replace with the project names you want to include
# include_project_names = ['PBOffice', 'OYOTownHouse', 'PerfectPanthea', 'PepsiRamNagar', 'PerfectMadhavaNivas', 'PerfectPrima',
#                          'PalmshoreGuestHouse', 'RajkumarSulakchana', 'PerfectPushparathi', 'JayalakshmiNagar', 'PerfectPrajana',
#                          'PerfectPrajaya', 'PerfectAswin', 'PerfectPrecise']

include_project_names = ['PerfectPlacid']

# Apply combined filtering:
# 1. Exclude rows where 'BillType' is 'Internal'
# 2. Include only rows where 'MaterialType' has values in include list
# 3. Include only rows where 'ProjectName' has values in include list
filtered_df = df[
    (df['BillType'] == 'External') &
    (df['MaterialType'].isin(include_material_types)) &
    (df['ProjectName'].isin(include_project_names))
]

# Save the filtered data to a new Excel file
filtered_df.to_excel(output_file, index=False)

print(f"Filtered data saved to {output_file}")
