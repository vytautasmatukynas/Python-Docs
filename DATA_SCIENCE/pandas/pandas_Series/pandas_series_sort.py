import pandas as pd


number = pd.Series([1, 8, 52, 3, 7, 40])
print(number)
print(number.sort_values())
print(number.sort_values(ascending=False))


data = pd.read_csv('Location.csv')
print(data)
print(data.shape)
# convert datasframe to series with squeeze()
data_ = data.squeeze()
print(data_)
print(data_.sort_values(ascending=False))
print(data_.shape)