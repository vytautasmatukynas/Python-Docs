import pandas as pd

# get index info and index name
data = pd.read_csv('Region.csv')
data_ = data.squeeze()

print(data_.index)
print(data_.name)
print(data_.index.name)

data_.index.name = "New"
print(data_.index.name)

# create numpy array
data_np = data_.index.to_numpy()
print(data_np)

# sort by index
data_2 = data_.sort_values(ascending=True)
data_head = data_2.head()
print(data_head)
# sort by index and gets only index
print(data_head.index.sort_values())
# sort by index and doesn't change dataset construction
print(data_head.sort_index())


