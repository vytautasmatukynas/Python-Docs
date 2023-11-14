names = ["Jonas", "Petras", "Stasys"]

import random
number = random.randint(0, 100)
student_score = {i: number for i in names}
print(student_score)

passed_names = {i: number for (i, number) in student_score.items() if number < 50}
print(passed_names)

temps = {"monday": 20,
        "friday": 30}

new_temp = {day: temp * 2 for (day, temp) in temps.items()}
print(new_temp)

users = [
        (0, 'aa', 'oo'),
        (1, 'ii', 'xx'),
]

username_mapping = {user[0]: user[1:3] for user in users}
print(username_mapping)


username, password = username_mapping[0]

if username == 'aa' and password == 'oo':
        print("URA")

else:
        print("O NOOP")

if username == 'aa' and password != 'None':
        print("O NOO")

