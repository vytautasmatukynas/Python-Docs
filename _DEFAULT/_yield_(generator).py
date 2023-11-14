# The yield statement suspends a function’s execution and sends a value back to the caller, but retains enough state
# to enable the function to resume where it left off. When the function resumes, it continues execution immediately
# after the last yield run. This allows its code to produce a series of values over time, rather than computing them
# at once and sending them back like a list.

# An infinite generator function that prints
# next square number. It starts with 1
def nextSquare():
    i = 1
    # An Infinite loop to generate squares
    while True:
        yield i * i
        i += 1  # Next execution resumes
        # from this point
# Driver code to test above generator
# function
for num in nextSquare():
    if num > 5:
        break
    print(num)

# <OR>

from time import sleep
def sample():
    for i in range(20):
        sleep(.5)
        yield i

# Creating a generator object
gen = sample()

# Iterating over the generator and printing the values
for num in gen:
    if num == 5:
        print("5<-")
        break
    print(num)


# A generator function that yields 1 for the first time,
# 2 second time and 3 third time
def simpleGeneratorFun():
    yield 1
    yield 2
    yield 3
# Driver code to check above generator function
for value in simpleGeneratorFun():
    print(value)

# <OR>

def first_call():
    return print("a")
def second_call():
    return print("b")
def third_all():
    return print("c")

# can use generators on funtions like this. This will wait till first func is finished and starts second and etc.
def api_calls():
    first_call()
    yield
    second_call()
    yield
    third_all()

# Iterate through the generator to trigger the function calls
for _ in api_calls():
    pass






