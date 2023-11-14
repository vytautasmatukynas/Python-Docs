"""
---> Syntax: sorted(iterable, key=None, reverse=False) <---
sorted() function is used to sort an iterable (e.g., a list, tuple, or string)
in ASC/DESC order. It returns a new sorted list and leaves the original
iterable unchanged.
"""
# Create a list of numbers
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
# Use the sorted() function to sort the numbers in ascending order
sorted_numbers = sorted(numbers)
# Print the sorted list of numbers
print(sorted_numbers)

# Create a list of numbers
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
# Use the sorted() function to sort the numbers in descending order
sorted_numbers_desc = sorted(numbers, reverse=True)
# Print the sorted list of numbers in descending order
print(sorted_numbers_desc)