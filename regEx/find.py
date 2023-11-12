import re

"""
findall() - Returns a list containing all matches
"""

# Print a list of all matches:
txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)

# Return an empty list if no match was found:
txt = "The rain in Spain"
x = re.findall("Portugal", txt)
print(x)

