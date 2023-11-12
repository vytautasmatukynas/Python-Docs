list = []
x = 1

while x < 100:

    if x % 3 == 0 and x % 5 == 0:
        list.append("fizzbuzz")
    elif x % 3 == 0:
        list.append("fizz")
    elif x % 5 == 0:
        list.append("buzz")
    else:
        list.append(x)

    x += 1

print(list)


list = []
for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        list.append('fizzbuzz')
    elif i % 3 == 0:
        list.append("fizz")
    elif i % 5 == 0:
        list.append("buzz")
    else:
        list.append(i)

print(list)