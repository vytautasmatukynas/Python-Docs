import numpy as np


array_a = np.array([1, 2, 3])
array_a
array_b = np.array([[1], [2]])
array_b
matrix_c = np.array([[1, 2, 3], [4, 5, 6]])
matrix_c

# add arrays
np.add(array_a, matrix_c)
np.add(array_b, matrix_c)
np.add(array_b, matrix_c, dtype=float)

# column mean
np.mean(matrix_c, axis=0)
# row mean
np.mean(matrix_c, axis=1)

# create array in range
a_range = np.arange(30)
a_range

# start from 0 and stop at 30
a_range = np.arange(start=0, stop=30)
a_range

# start from 0 and stop at 30 and step is every second char
a_range = np.arange(start=0, stop=30, step=2)
a_range

# start from 0 and stop at 30 and step is every second char and add type
a_range = np.arange(start=0, stop=30, step=2, dtype=float)
a_range