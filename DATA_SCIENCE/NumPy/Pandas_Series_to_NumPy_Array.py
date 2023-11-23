import pandas as pd
import numpy as np


prices = pd.Series({"A": 25, "C": 45, "B": 35})
print(prices)
# Pandas array
pandas_array = prices.array
print(pandas_array)
print(pandas_array[0])

# convert to numpy array
numpy_array = prices.to_numpy()
print(numpy_array)
print(numpy_array[0])
# add type to array values
numpy_array = prices.to_numpy(dtype=str)
print(numpy_array)
print(numpy_array[0])
numpy_array = prices.to_numpy(dtype=float)
print(numpy_array)
print(numpy_array[0])