"""
---> Syntax: map(function, iterable_element) <---
map() function returns a map object(which is an iterator) of the results after applying the given function to each
item of a given iterable (list, tuple etc.). 
"""
# Define a function that doubles numbers
def addition(n):
    return n * 2

# We double all numbers using map()
tuple_numbers = (1, 2, 3, 4)
# Use map to apply the function to each element in the list

result = map(addition, tuple_numbers)
# print map() object
print(result)
# convert map() object to list
double_numbers = list(result)
print(double_numbers)

# Define a function that doubles even numbers and leaves odd numbers as is
def double_even(num):
    if num % 2 == 0:
        return num * 2
    else:
        return num
# Create a list of numbers to apply the function to
list_numbers = [1, 2, 3, 4, 5]
# Use map to apply the function to each element in the list
result = map(addition, tuple_numbers)
# print map() object
print(result)
# convert map() object to set
double_numbers = set(result)
print(double_numbers)

# List of strings
list_text = ['sat', 'bat', 'cat', 'mat']
# map() can listify the list of strings individually
test = list(map(list, list_text))
print(test)



