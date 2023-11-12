"""
enumerate() function is used to iterate over an iterable
while keeping track of the index (position) of the current item.
"""

fruits = ["apple", "banana", "cherry"]

# Iterate over the 'fruits' list using 'enumerate()'
# 'index' will store the index of the current fruit, and 'fruit' will store the fruit itself.
for index, fruit in enumerate(fruits):
    # 'index' is the index of the current fruit (0 for "apple", 1 for "banana", 2 for "cherry").
    # 'fruit' is the name of the current fruit.

    # Print the index and the fruit using an f-string.
    # This will display the index and the fruit name together in the output.
    print(f"Index {index}: {fruit}")