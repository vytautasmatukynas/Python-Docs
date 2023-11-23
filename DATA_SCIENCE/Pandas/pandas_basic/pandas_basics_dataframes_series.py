############ SERIES ###################
import pandas as pd

# create label based index
index = ['A', 'B', 'C', 'D']
products = [1, 2, 3, 4]

# Create pandas series
product_categories = pd.Series(products, index)
print(product_categories)
print(product_categories.index)

print("\n")

# with position based index
product_categories = pd.Series(products)
print(product_categories)
print(product_categories.index)

print("\n")

import numpy as np

array_a = np.array([1, 2, 5, 4, 5])
print(array_a)
series_a = pd.Series(array_a)
print(series_a)

print("\n")

# check data types
print(series_a.dtype)
# check data size
print(series_a.size)
print("\n")
print(series_a[1])

print("\n")

prices = pd.Series({"ooo": 5, "aaa": 4, "eee": 6})
print(prices)
print(prices.index)
#################################################
print("\n")
prices = pd.Series({"ooo": 5, "aaa": 4, "eee": 6,
                    "ooo0": 5, "a0aa": 4, "ee0e": 6,
                    "oo0o0": 5, "aa0a": 4, "ee00e": 6})
print(prices.sum())
print(prices.min())
print(prices.max())
print("\n")
# print label of max and min values in data set
print(prices.idxmax())
print(prices.idxmin())
print("\n")
# print first 5 rows
print(prices.head())
# print last 5 rows
print(prices.tail())
#########################################################

print("\n")

#################### DATAFRAMES ####################
# create basic DataFrame
dict = {"name": ["Steve", "John"],
        "score": [45, 56]}
indexes = [1, 2]
name_indexes = ["first", "secod"]

dict_frame = pd.DataFrame(dict, index=[1, 2])
dict_frame_2 = pd.DataFrame(dict, indexes)
dict_frame_3 = pd.DataFrame(dict, name_indexes)

print(dict_frame)
print("\n")
print(dict_frame_2)
print("\n")
print(dict_frame_3)

index = [1, 2, 3, 4]
products = ['A', 'B', 'C', 'D']
product_categories = pd.Series(products, index)
data = {'Number': index, "Letter": products}
dataframe_ = pd.DataFrame(data, index)
print(dataframe_)

print("\n")

df = pd.DataFrame(data=[["OOOO", 500], ["AAAA", 4000], ["BBBB", 6000]],
                  columns=["NAME", "NUMBER"],
                  index=["A", "B", "Z"])
print(df)

print(df.shape)

print("\n")

df_2 = pd.DataFrame(data=[[5, 500], [6, 4000], [7, 6000]],
                  columns=["NAME", "NUMBER"],
                  index=[1, 2, 3])
print(df_2)

print(df_2.shape)