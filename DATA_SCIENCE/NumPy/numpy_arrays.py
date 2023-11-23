import numpy as np

matrix_c = np.array([[1, 2, 3], [4, 5, 6]])
matrix_c

# create empty array
a_empty = np.empty(shape=(2, 3))
a_empty

# create "0" array
a_zeros = np.zeros(shape=(2, 3))
a_zeros

# create "1" array
a_ones = np.ones(shape=(2, 3))
a_ones

# create array with value you want
a_full = np.full(shape=(2, 3), fill_value=5)
a_full

# create array full of zeros with shape like matrix_c
# can create _full _ones _zeros _empty
array_like_matrix = np.zeros_like(matrix_c)
array_like_matrix