import pandas as pd
import os

# Directory containing the input Excel files
# Replace with the path to your input directory
input_directory = r'D:\IGS\Constrogen_data_migration\files\bills\in_progress_projects_stock_records'
output_file = r'D:\IGS\Constrogen_data_migration\files\bills\in_progress_projects_stock_records\combined\combined_in_progress_projects_stock_records.xlsx'  # Output file name

# List to store DataFrames from each file
combined_data = []

# Loop through each file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):  # Check for Excel files
        file_path = os.path.join(input_directory, filename)
        # Read the Excel file
        # Adjust the sheet name if necessary
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        combined_data.append(df)  # Append the DataFrame to the list

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(combined_data, ignore_index=True)

# Save the combined DataFrame to a new Excel file
combined_df.to_excel(output_file, index=False)

print(f"Combined data saved to {output_file}")
