import pandas as pd
import numpy as np


array_1 = np.array([[1, 2, 3], [5, 8, 9]])
dataframe_1 = pd.DataFrame(array_1)
print(dataframe_1)

dataframe = pd.DataFrame(array_1, columns=['A', 'B', 'C'], index=["Row_1", "Row_2"])
print(dataframe)

data = pd.read_csv('Lending-company.csv', index_col="LoanID")
# create copy that main file won't be changed
lending_data = data.copy()
print(lending_data)
# print column names
print(lending_data.columns)
# print data types in columns
print(lending_data.dtypes)
# print data values
print(lending_data.values)
# print table size
print(lending_data.shape)

numpy_data = lending_data.to_numpy()
print(numpy_data)