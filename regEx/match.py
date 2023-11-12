import re

"""
match() function to search pattern within the test_string. The method returns a match object 
if the search is successful. If not, it returns None.
"""

pattern = '^a...s$'
test_string = 'abyss'
result = re.match(pattern, test_string)

if result:
  print("Search successful.")
else:
  print("Search unsuccessful.")