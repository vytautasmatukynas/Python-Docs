"""
The assert statement in Python is used as a debugging aid to test whether a given condition is true. If the condition
is false, an AssertionError exception is raised, indicating that something unexpected has happened. It's often used to
catch programming errors early in development.
"""

def calculate_average(numbers):
    # Use an assert statement to check if the length of the "numbers" list is greater than 0
    assert len(numbers) > 5, "Length cannot be more then 5"
    total = sum(numbers)
    return total / len(numbers)

data = [10, 20, 30, 40, 50]
result = calculate_average(data)
print("Average:", result)
