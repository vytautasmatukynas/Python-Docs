import re

""" 
span() - this method returns a tuple containing starting and ending index of the matched string 
"""

# Print the position (start- and end-position) of the first match occurrence.
# The regular expression looks for any words that starts with an upper case "S":
txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span()) # returns a tuple