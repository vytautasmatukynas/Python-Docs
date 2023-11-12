import re

"""
group() - this method returns a tuple containing all the subgroups of the match
"""

# Print the part of the string where there was a match.
# The regular expression looks for any words that starts with an upper case "S":
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group()) # returns a tuple