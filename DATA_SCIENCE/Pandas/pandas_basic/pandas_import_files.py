import pandas as pd


data = pd.read_csv('Lending-company.csv')
print(data)

data = pd.read_csv('Lending-company.csv', index_col='LoanID')
print(data)