"""
---> Syntax: filter(function, iterable_element) <---
filter() function in Python is used to filter elements from an iterable
(e.g., a list, tuple, or other collection) based on a specified condition.
It creates a filter object that is an iterable containing only the elements
that meet the condition.
"""
# Define a function to check if a number is even
def is_even(x):
    return x % 2 == 0

# Create a list of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Use the filter() function to filter out even numbers from the list
filtered_numbers = filter(is_even, numbers)

# Convert the filter object to a list for printing
result_list = list(filtered_numbers)

# Print the list of filtered even numbers
print(result_list)