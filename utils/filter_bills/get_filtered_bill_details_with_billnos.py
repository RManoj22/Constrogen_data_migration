import pandas as pd

filtered_bills_header = r'D:\IGS\Constrogen_data_migration\files\bills\filtered_bills\filtered_bill_header.xlsx'

combined_stock_records = r'D:\IGS\Constrogen_data_migration\files\bills\in_progress_projects_stock_records\combined\combined_in_progress_projects_stock_records.xlsx'

output_file = r'D:\IGS\Constrogen_data_migration\files\bills\filtered_bills\filtered_bill_detail.xlsx'

bills_df = pd.read_excel(filtered_bills_header)
stocks_df = pd.read_excel(combined_stock_records)

boolean_series = stocks_df['BillNO'].isin(bills_df['BillNo'])

filtered_stocks_df = stocks_df[boolean_series]

filtered_stocks_df.to_excel(output_file, index=False)


print(f"Filtered data saved to {output_file}")
