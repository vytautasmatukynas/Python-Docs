""" zip object to one zipped object.
If some object has less items then other, then it will zip
just till last item in that object and stops zipping"""

list_1 = [1, 5]
tuple_1 = (8, 9, 15)
set_1 = {7, 8}
dict_1 = {"kazkas": "kazko"}

print(list(zip(list_1, tuple_1, set_1)))
# by default zips keys from dict
print(list(zip(list_1, tuple_1, set_1, dict_1)))
# you can specify what to zip in dict
print(list(zip(list_1, tuple_1, set_1, dict_1.keys())))
print(list(zip(list_1, tuple_1, set_1, dict_1.values())))

value_1 = "kazkas"
value_2 = "kazkur"
print(list(zip(value_2, value_1)))

# Two lists, 'names' and 'scores', containing student names and their respective scores.
names = ["Alice", "Bob", "Charlie"]
scores = [90, 85, 88]

# Use 'zip()' to combine the two lists element-wise, creating pairs of corresponding names and scores.
# The first iteration will pair "Alice" with 90, the second with "Bob" and 85, and the third with "Charlie" and 88.
for name, score in zip(names, scores):
    # 'name' stores the student's name, and 'score' stores their corresponding score.

    # Print the student's name and score together using an f-string.
    # This will display the name and score in the output.
    print(f"{name}: {score}")
