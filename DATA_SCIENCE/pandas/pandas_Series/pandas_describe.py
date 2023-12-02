import pandas as pd


data = pd.read_csv("Location.csv")

# data info
print(data.describe())
print(len(data))
print(data.nunique())

