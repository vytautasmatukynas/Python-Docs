import numpy as np

# scalar is 0D (tensor rank 0)
# vector is 1D (tensor rank 1)
# matrix is 2D (tensor rank 2)
# multiple matrices is 3D (tensor rank 3)

# list with 1 item (scalar)
scalar = [5]

# lists (vectors). There can be column vector and row vector
vector_1 = np.array([1, 5, 7])
vector_2 = np.array([2, 5, 9])

# create numpy array (matrix) from few tables
matrix_1 = np.array([vector_1, vector_1])
matrix_2 = np.array([vector_2, vector_2])

# few matrices in one array - tensor
tensor_3 = np.array([matrix_1, matrix_2])

print(matrix_1)
print(matrix_2)
print(tensor_3)

# (2, 3) is matrix with 2 rows and 3 columns
print(matrix_1.shape)
print(matrix_2.shape)
# (2, 2, 3) is 2x matrices with 2 rows and 3 columns
print(tensor_3.shape)

######################################################

# math with vectors
vector_1 = np.array([1, 5, 7])
vector_2 = np.array([2, 5, 9])

# multiple vectors by using ".dot" 1*2+5*5+7*9=90
print(np.dot(vector_1, vector_2))
# multiple vector by one number
print(5 * vector_1)
# subtrackting vectors [2-1, 5-5, 9-7]
print(vector_2 - vector_1)
# adding vectors [2+1, 5+5, 9+7]
print(vector_2 + vector_1)

###############################################################

matrix_1 = np.array([vector_1, vector_1])
matrix_2 = np.array([vector_2, vector_2, vector_2])

print(matrix_1)
print(matrix_2)
print(matrix_1.shape)
print(matrix_2.shape)

# multiple metrices by using ".dot":
# 1*2+5*2+7*2, 1*5+5*5+7*5, 1*9+9*5+7*9
# 1*2+5*2+7*2, 1*5+5*5+7*5, 1*9+9*5+7*9
print(np.dot(matrix_1, matrix_2))
# Result:
# 26  65 117
# 26  65 117
