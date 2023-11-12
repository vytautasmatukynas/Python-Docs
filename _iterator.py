"""
An iterator is an object that contains countable number of values.
Lists, tuples, dictionaries, and sets are all iterable objects. They are iterable containers
which you can get an iterator from. All these objects have a iter() method which is used to get an iterator.
"""

# Return an iterator from a tuple, and print each value:
tuple = ("apple", "banana", "cherry")
iterator = iter(tuple)

while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break


# Strings are also iterable objects, containing a sequence of characters:
text = "banana"
iterator = iter(text)

while True:
    try:
        item = next(iterator)
        print(item)
    except StopIteration:
        break
