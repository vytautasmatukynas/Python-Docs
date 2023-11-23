import numpy as np


array_a = np.array([[1, 2, 3], [4, 5, 6]])
array_a

# to float numbers
array_a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float64)
array_a

# to complex number format
array_a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.complex64)
array_a

# to bool type, 0 = False
array_a = np.array([[0, 2, 3], [0, 5, 6]], dtype=np.bool_)
array_a

# to string
array_a = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.str_)
array_a

# unicode with 2 elements, only shows 2 elements
array_a = np.array([[1, 2, 3], [4, 5, 666]], dtype='<U2')
array_a
