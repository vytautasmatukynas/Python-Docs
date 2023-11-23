import pandas as pd


data = pd.read_csv("Sales-products.csv", index_col="SaleID")
data_copy = data.copy()
print(data_copy.head(10))
# select column you want
print(data_copy['Quantity'].tail(10))
col_to_sort = ['OrderMethod', 'Quantity']
print(data_copy[col_to_sort].head())



