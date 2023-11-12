"""
Syntax: any(iterable), all(iterable)
any() function returns True if at least one element in an iterable is True.
all() function returns True if all elements in an iterable are True.
"""

values = [True, False, True, True]
any_true = any(values)  # True
all_true = all(values)  # False

""" 
--> SAMPLE <--- 
"""
# List of student eligibility data, where each element is a tuple (name, age, grade_point_average)
student_eligibility_data = [
    ("Alice", 18, 3.8),
    ("Bob", 17, 3.5),
    ("Charlie", 19, 4.0)
]
# Check if any student meets the age requirement (e.g., 18 years or older)
is_any_student_eligible_age = any(age >= 18 for _, age, _ in student_eligibility_data)

# Check if all students meet the grade point average requirement (e.g., GPA of 3.5 or higher)
are_all_students_eligible_gpa = all(gpa >= 3.5 for _, _, gpa in student_eligibility_data)

# Output the results
if is_any_student_eligible_age:
    print("At least one student meets the age requirement.")
else:
    print("No student meets the age requirement.")

if are_all_students_eligible_gpa:
    print("All students meet the GPA requirement.")
else:
    print("Not all students meet the GPA requirement.")
