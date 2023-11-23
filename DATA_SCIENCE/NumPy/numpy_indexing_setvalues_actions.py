import numpy as np

array_a = np.array([[1, 2, 3], [4, 5, 6]])

# index like list
array_a[0]
array_a[0][1]
# index numpy method
array_a[0, 1]


# index like list
array_a[1]
array_a[1][1]
# index numpy method
array_a[1, 1]

# get first column values
array_a[:,0]

# change value of 1 item
array_a[1, 0] = 9
array_a

# change all array
array_a[1] = [7, 8, 9]
array_a

# change all values to "9"
array_a[0] = 9
array_a

# change fist column of array
array_a[:,0] = 10
array_a

# change all values
array_a[:] = 10
array_a

# do some action with all values
array_b = array_a[:] / 2
array_b

array_c = array_b + 5
array_c

# do some action to multiple arrays
array_d = array_c + array_b
array_d

array_d = array_c[0] * array_b
array_d