"""Dictionaries are used to store data values in key:value pairs.
A dictionary is a collection which is ordered, changeable and do not allow duplicates."""

# dictionary.get(keyname, value)
# keyname 	Required. The keyname of the item you want to return the value from
# value 	Optional. A value to return if the specified key does not exist.
#           Default value None
car = {
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}
x = car.get("model")
# Get the value of the "model" item:
print(x)
# Try to return the value of an item that do not exist:
x = car.get("price", 15000)
print(x)
x = car.get("model", 15000)
print(x)


dict = {
    "M7": 6,
    "M8": 7,
    "M9": 6
}
print(dict)
print(dict["M7"])

a = dict.get("M7")
print(a)

a = dict.keys()
print(a)

a = dict.values()
print(a)

a = dict.items()
print(a)

print(len(dict))
print(type(dict))
# thisdict = dict(name="John", age=36, country="Norway")
# print(thisdict)

# Dict with list value.
dict_list = {
    "M7": 6,
    "M8": 7,
    "M9": [6, 7, 8]
}

print(dict_list)
print(dict_list["M9"])

# Print value selected from dict with list index.
print(dict_list["M9"][0])

# Add item to dict.
dict["M10"] = 8
print(dict)

dict.update({"M14": 200})
print(dict)

# Change value.
dict["M10"] = 12
print(dict)

dict.update({"M14": 189})
print(dict)

# If/in.
if "M7" in dict:
    print("Yes, 'M7' is one of the keys in the 'dict' dictionary")

# The pop()/del method removes the item with the specified key name.
dict.pop("M7")
print(dict)

del dict["M10"]

# The popitem() method removes last item.
dict.popitem()
print(dict)

# Del all dict.
del dict

# Delete all items from dict.
dict = {
    "M7": 6,
    "M8": 7,
    "M9": 10
}

dict.clear()
print(dict)

# Loop dict.
dict = {
    "M7": 6,
    "M8": 7,
    "M9": 10
}

for x in dict:
    print(x)

for x in dict:
    print(dict[x])

for x in dict.values():
    print(x)

for x in dict.keys():
    print(x)

for x, y in dict.items():
    print(x, y)

# Copy dict.
mydict = dict.copy()
print(mydict)

# mydict = dict(dict)
# print(mydict)

# Nested dict.
dict = {
    "hole":
        {"M7": 6,
         "M8": 7,
         "M9": 10},
    "valve":
        {"h7": 6,
         "h8": 7,
         "h9": 10}
}
print(dict)
print(dict["hole"])
print(dict["hole"].keys())
print(dict["hole"].values())

hole = {"M7": 6,
        "M8": 7,
        "M9": 10}
valve = {"h7": 6,
         "h8": 7,
         "h9": 10}
dict = {
    "hole": hole,
    "valve": valve
}
print(dict)
