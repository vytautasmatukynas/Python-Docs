# list_a = [1, 8, 9, 20]
#
# # square all numbers and vreate list with values of it
# list_b = [n**2 for n in list_a]
#
# print(list_b)
#
# # just even numbers
# list_c = [n for n in list_a if n % 2 == 0]
# print(list_c)

with open("list_comprehension/file1.txt", 'r') as file1:
    file1_data = file1.readlines()
    list1 = [int(i.strip()) for i in file1_data]
    print(list1)

with open("list_comprehension/file2.txt", 'r') as file2:
    file2_data = file2.readlines()
    list2 = [int(i.strip()) for i in file2_data]
    print(list2)


list3 = [number2 for number2 in list2 if number2 in list1]
print(list3)