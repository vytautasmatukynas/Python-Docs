import pandas as pd

# get product data by index. Similar to slicing list and etc.
data = pd.read_csv('Lending-company.csv', index_col='LoanID')
data_copy = data.copy()
print(data_copy.head())

print("\n")

# get data of second row
print(data_copy.iloc[1])

print("\n")

# get second row third column data
print(data_copy.iloc[1, 2])

print("\n")

# get data of second row
print(data_copy.iloc[1, :])

print("\n")

# get data of second column
print(data_copy.iloc[:, 1])

print("\n")

# get products column second value
product_data = data_copy["Product"]
print(product_data.iloc[1])
