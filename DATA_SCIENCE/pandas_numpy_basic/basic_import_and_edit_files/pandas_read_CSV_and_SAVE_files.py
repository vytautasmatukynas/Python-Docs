import pandas as pd

file = 'Lending-company.csv'
data = pd.read_csv(file, usecols=['StringID', 'Location'], index_col=["StringID"])
print(data.head())

data.to_csv("csvfile.csv")
data.to_json("jsonfile.json")
data.to_excel("excelfile.xlsx")
data.to_excel("excelfile_noindex.xlsx", index=False)