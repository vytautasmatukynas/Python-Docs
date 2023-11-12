import re

"""
sub() - function replaces the matches with the text of your choice
"""

# Replace every white-space character with the number 9:
txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)

# Replace the first 2 occurrences:
txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)