"""Tuples are used to store multiple items in a single variable.
Tuple items are ordered, unchangeable, and allow duplicate values.
Tuples are unchangeable, meaning that we cannot change, add or remove items after the tuple has been created.
Tuple items can be of any data type: strings, integers and boolean.
"""

tuple = (4, "b", "a", 8, True)
print(type(tuple))
print(tuple)
print(len(tuple))

# Using the tuple() method to make a tuple.
# mytuple = tuple((4, "b", "a", 8, True)) # note the double round-brackets
# print(mytuple)

# Search tuple.
if "b" in tuple:
  print("Yes, 'b' is in tuple")

# Unpack tuple.
(a, b, c, d, e) = tuple
(a, b, *c, e) = tuple
print(a)
print(c)
print(*tuple)

# Access tuple items by index.
print(tuple[1])
print(tuple[-1])
print(tuple[1:2])
print(tuple[:1])
print(tuple[1:])

# Convert the tuple into a list to be able to change it.
# y = list(tuple)
# y[1] = "kiwi"
# tuple = tuple(y)
# print(tuple)

# Convert the tuple into a list, add/remove item, and convert it back into a tuple.
# y = list(tuple)
# y.append("c")
# tuple = tuple(y)

y = ("d",)
tuple += y
print(tuple)

# y = list(tuple)
# y.remove("e")
# thistuple = tuple(tuple)

# Delete tuple
del tuple

# Loop tuple.
tuple = (4, "b", "a", 8, True)

for i in tuple:
  print(i)

# Print all items by referring to their index numbe.
for i in range(len(tuple)):
  print(i)

# Print all items, using a while loop to go through all the index numbers.
i = 0
while i < len(tuple):
  print(i)
  i += 1

# Join 2 tuples and multiple tuple.
tuple1 = ("a", "b" , "c")
tuple2 = (1, 2, 3)
tuple3 = tuple1 + tuple2
print(tuple3)

mytuple = tuple * 2
print(mytuple)