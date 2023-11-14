from functools import reduce

""" 
Syntax: reduce(function, iterable, initial)
reduce() function is used to apply a rolling computation to 
sequential pairs of values in an iterable, ultimately reducing 
it to a single value.
"""
# List of numbers
numbers = [1, 2, 3, 4, 5]

# Use 'reduce()' to calculate the product of all elements in the 'numbers' list
# The lambda function multiplies 'x' and 'y' for each element in the list.
product = reduce(lambda x, y: x * y, numbers)

# Print the product
print(product)