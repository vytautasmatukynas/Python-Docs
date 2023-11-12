import re

"""
search() - Returns a Match object if there is a match anywhere in the string
"""

# Search the string to see if it starts with "The" and ends with "Spain":
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)
print(x)
if x:
  print("YES! We have a match!")
else:
  print("No match")

# Search for the first white-space character in the string:
txt = "The rain in Spain"
x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start())

# Do a search that will return a Match Object:
txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) #this will print an object

# Print the position (start- and end-position) of the first match occurrence.
# The regular expression looks for any words that starts with an upper case "S":
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span()) # returns a tuple containing starting and ending index of the matched string

# Print the string passed into the function:
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)

# Print the part of the string where there was a match.
# The regular expression looks for any words that starts with an upper case "S":
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group()) # This method returns a tuple containing all the subgroups of the match