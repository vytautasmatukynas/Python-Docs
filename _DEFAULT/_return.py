# A return statement is used to end the execution of the function call and “returns” the result (value of the
# expression following the return keyword) to the caller. The statements after the return statements are not
# executed. If the return statement is without any expression, then the special value None is returned. A return
# statement is overall used to invoke a function so that the passed statements can be executed.

def add(a, b):
    # returning sum of a and b
    return a + b
def is_true(a):
    # returning boolean of a
    return bool(a)
# calling function
res = add(2, 3)
print("Result of add function is {}".format(res))
res = is_true(2 < 5)
print("\nResult of is_true function is {}".format(res))

# A Python program to return multiple
# values from a method using class
class Test:
    def __init__(self):
        self.str = "geeksforgeeks"
        self.x = 20
    # This function returns an object of Test
def fun():
    return Test()
# Driver code to test above method
t = fun()
print(t.str)
print(t.x)