"""Since lists are indexed, lists can have items with the same value.
List items can be of any data type - string, int and boolean."""

list = [1, "a", "b", 2, "b", True]
print(list)

# It is also possible to use the list() constructor when creating a new list.
# mytuple = (1, "a", "b", 2, "b", True)
# mylist = list((1, "a", "b", 2, "b", True))
# print(mylist)
# mylist = list(mytuple)
# print(mylist)

# Print the number of items in the list.
print(len(list))

# Print list in reverse order.
list.reverse()
print(list)

# Check type.
print(type(list))

# Select items from list.
print(list[0])
print(list[-1])
print(list[::-2])
print(list[::-3])
print(list[1:3])
print(list[::3])
print(list[1:4:2])
print(list[:3])
print(list[2:])

# Search for item in list
a = "a"
if a in list:
    print(f'there is {a} in list')
else:
    print(f"there is no {a} in list")

# To change the value of a specific item, refer to the index number.
list[1] = "c"
print(list)

# Change values in list by index.
list[1:2] = ["c", "d"]
print(list)
list[1:2] = ["f"]
print(list)

# Index list items.
for item in list:
    a = list.index(item)
    print(a)

# The insert() method inserts an item at the specified index.
# Index number + list item.
list.insert(3, "AAA")
print(list)

# To add an item to the end of the list, use the append() method.
list.append("BBB")
print(list)

# To append elements from another list to the current list, use the extend() method.
# The extend() method does not have to append lists, you can add any iterable object (tuples, sets, dictionaries etc.).
mylist = ["go", "good"]
mytuple = ("bad", "away")

list.extend(mylist)
print(list)
list.extend(mytuple)
print(list)

# The remove() method removes the specified item.
list.remove("go")
print(list)

# The pop() method removes the specified index.
list.pop(0)
print(list)

# If you do not specify the index, the pop() method removes the last item.
list.pop()
print(list)

# The del keyword also removes the specified index or all list - "del list".
del list[0]
print(list)

# The clear() method empties the list.
list.clear()
print(list)

list = [1, "a", "b", 2, "b", True]

# Loop list items.
for item in list:
    print(item)

# Loop through the list items by referring to their index number.
# Lange() and len() functions to create a suitable iterable.
for i in range(len(list)):
    print(i)

# Loop through the list items by using a while loop.
# len() function to determine the length of the list
# Print all items, using a while loop to go through all the index numbers
i = 0
while i < len(list):
    print(list[i])
    i += 1

# A short hand for loop that will print all items in a list.
[print(i) for i in list]

# List comprehension offers a shorter syntax when you want to create a new list based on the values of an existing list.
list = ["ananasas", "b", "bananas"]
newlist = []
for x in list:
    if "a" in x:
        newlist.append(x)
print(newlist)

# newlist = [expression for item in iterable if condition == True].
newlist = [x for x in list if "a" in x]
print(newlist)

newlistindex = [x[0] for x in list]
print(newlistindex)

# Create list with range().
newlistrange = [x for x in range(10)]
print(newlistrange)

newlistrange_less = [x for x in range(10) if x < 5]
print(newlistrange_less)

# Using upper/lower.
newlistupper = [x.upper() for x in newlist]
print(newlistupper)

# Set all values in the new list to 'hello'.
list = ['hello' for x in newlist]
print(list)

list = ["ananasas", "b", "bananas"]
newlistoflist = [x if x != "ananasas" else "orange" for x in list]
print(newlistoflist)

# List sort().
# By default the sort() method is case sensitive,
# resulting in all capital letters being sorted before lower case letters.
# Case-insensitive sort function, use str.lower as a key function

thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort()
print(thislist)

thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)

thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key=str.lower)
print(thislist)

thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)

thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist.sort(reverse=True)
print(thislist)

thislist = [100, 50, 65, 82, 23]
thislist.sort(reverse=True)
print(thislist)

thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)

# Make a copy of a list with the copy() method.
thislist = ["apple", "banana", "cherry"]
mylist = thislist.copy()
print(mylist)

# thislist = ["apple", "banana", "cherry"]
# mylist = list(thislist)
# print(mylist)

# Join multiple list to one.
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]
list3 = list1 + list2
print(list3)

list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

for x in list2:
    list1.append(x)

print(list1)