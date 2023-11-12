import re

"""
split() - function returns a list where the string has been split at each match
"""

# Split at each white-space character:
txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)

# You can control the number of occurrences by specifying the maxsplit parameter:
txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)