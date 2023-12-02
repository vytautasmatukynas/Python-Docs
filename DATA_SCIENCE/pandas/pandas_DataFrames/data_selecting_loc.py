import pandas as pd


data = pd.read_csv('Lending-company.csv', index_col='StringID')
data_copy = data.copy()
print(data_copy.head())

print("\n")

# get row data
data_row_loadid_3 = data.loc['LoanID_3']
print(data_row_loadid_3)

print("\n")

# get selected and column cell value
data_cell_loadid_3_product = data.loc['LoanID_3', 'Product']
print(data_cell_loadid_3_product)

print("\n")

# get column data
data_col_locations = data.loc[:, 'Location']
print(data_col_locations)