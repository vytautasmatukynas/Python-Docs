"""
---> Syntax: lambda arguments : expression <---
lambda() function (also known as a lambda expression) is a way to define small,
anonymous functions using a compact syntax.
"""
# Simple anonymous lambda function
x = lambda i: i * i
print(x(5))
# OR
print((lambda x: x * x)(5))

# The expression does not need to always return a value. The following lambda function does not return anything.
greet = lambda name: print('Hello ', name)
greet('Steve')

# The following lambda function contains three parameters
sum = lambda x, y, z : x + y + z
num_sum = sum(5, 10, 15)
print(num_sum)

""" 
FILTER WITH LAMBDA 
"""
# Create a list of numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
# Use the filter() function with a lambda function to filter out even numbers from the list
filtered_numbers = filter(lambda x: x % 2 == 0, numbers)
# Convert the filter object to a list for printing
result_list = list(filtered_numbers)
# Print the list of filtered even numbers
print(result_list)

""" 
MAP WITH LAMBDA 
"""
# Create a list of numbers that we want to apply the function to
list_numbers = [1, 2, 3, 4, 5]

# Use a lambda function with the map() function to square each number in the list
# The lambda function defined here takes an input 'x' and returns 'x * x', which is the square of 'x'.
result = list(map(lambda x: x * x, list_numbers))

# Print the list of squared items
print(result)

# Add two lists using map and lambda
numbers_first = [1, 2, 3]
numbers_second = [4, 5, 6]
result = map(lambda x, y: x + y, numbers_first, numbers_second)
print(list(result))

# Use a lambda function with map() to square each number
squared_numbers_lambda = map(lambda x: x ** 2, numbers_first)
# Convert the map result into a list and print the squared numbers
print(list(squared_numbers_lambda))  # Output: [1, 4, 9, 16, 25]

"""
SORTED + LAMBDA
"""
# Create a list of fruits
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
# Use the sorted() function to sort the fruits based on their lengths
# The lambda function `lambda x: len(x)` calculates the length of each fruit's name and uses it as the sorting key
sorted_fruits = sorted(fruits, key=lambda x: len(x))
# Print the sorted list of fruits
print(sorted_fruits)

""" 
MAP + FILTER + SORTED + LAMBDA 
"""
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
# Use filter and lambda to keep only even numbers
even_numbers = filter(lambda x: x % 2 == 0, numbers)
# Use map and lambda to square the even numbers
squared_even_numbers = map(lambda x: x ** 2, even_numbers)
# Convert the map object to a list for printing
result_list = sorted(list(squared_even_numbers))
# Print the list of squared even numbers
print(result_list)