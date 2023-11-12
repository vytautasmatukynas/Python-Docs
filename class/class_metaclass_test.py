# metaclass is class of class. Class creates object how object behaves,
# metaclass creates how class behaves.
# have to make inherit from "type", that it would be metaclass

# Define a custom metaclass named Meta that inherits from "type"
class Meta(type):
    # This is called before the "__init__" method of the class
    def __new__(cls, class_name, bases, attrs):
        # Print the original attributes of the class
        print("Original attributes:", attrs)

        # Create a new dictionary 'a' to store modified attributes
        a = {}

        # Iterate through the attributes of the class
        for name, value in attrs.items():
            # Check if the attribute name starts with "__" (dunder methods)
            if name.startswith("__"):
                # Preserve dunder methods as they are
                a[name] = value
            else:
                # Change attribute names to uppercase and store them in 'a'
                a[name.upper()] = value

        # Print the modified attributes
        print("Modified attributes:", a)

        # Create a new class using the modified attributes and return it
        return super().__new__(cls, class_name, bases, a)

# Use the custom metaclass "Meta" to create a class named "cat"
class Cat(metaclass=Meta):
    # Define some attributes
    x = 5
    y = 6

    # Define a method
    def hello(self):
        print("hi")

# Create an instance of the "Cat" class
d = Cat()

# Attempt to access the "hello" method (note that it was modified to "HELLO" by the metaclass)
print("Calling HELLO method:")
d.HELLO()