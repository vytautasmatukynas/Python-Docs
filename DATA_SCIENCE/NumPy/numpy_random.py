from numpy.random import Generator as gen
from numpy.random import PCG64 as pcg

# always generates random arrays and matrices
arrays_RG = gen(pcg())
arrays_RG.normal(size=(5))
arrays_RG.normal(size=(5, 6))

# you can specify the seed and then this matrix or 
# array will be generated same. 
arrays_RG = gen(pcg(seed=555))
arrays_RG.normal(size=(5))
arrays_RG.normal(size=(5, 6))

# always generates random arrays and matrices
arrays_RG = gen(pcg())
arrays_RG.random(size=(5))
arrays_RG.random(size=(5, 6))

# values, proc. how many values should be of each, shape
arrays_RG = gen(pcg())
arrays_RG.choice([1, 2, 3], p = [0.3, 0.3, 0.4], size=(5))
arrays_RG.choice([1, 2, 3], p = [0.3, 0.3, 0.4], size=(5, 6))