# Superclass sample
class ParentClass:
    def custom_method(self):
        print("ParentClass custom method")

class ChildClass(ParentClass):
    def custom_method(self):
        super().custom_method()  # Calls the custom_method from the ParentClass using super()
        print("ChildClass custom method")

child_obj = ChildClass()  # Creates an instance of ChildClass
child_obj.custom_method()  # Calls the custom_method of the ChildClass


##########################################
# Define the ParentClass
class ParentClass:
    # Constructor (__init__) for ParentClass, takes a 'name' parameter
    def __init__(self, name):
        # Initialize an instance variable 'self.name' with the provided 'name'
        self.name = name
        # Print a message indicating that an instance of ParentClass has been initialized with the provided 'name'
        print(f"ParentClass initialized with name: {self.name}")

# Define the ChildClass as a subclass of ParentClass
class ChildClass(ParentClass):
    # Constructor (__init__) for ChildClass, takes 'name' and 'age' parameters
    def __init__(self, name, age):
        # Call the constructor of the parent class (ParentClass) using super()
        super().__init__(name)
        # Initialize an instance variable 'self.age' with the provided 'age'
        self.age = age
        # Print a message indicating that an instance of ChildClass has been initialized with the provided 'age'
        print(f"ChildClass initialized with age: {self.age}")

# Create an instance of ChildClass with the values "Alice" for 'name' and 25 for 'age'
child_obj = ChildClass("Alice", 25)


##########################################
# Define the ParentA class
class ParentA:
    # Method 'method' in ParentA
    def method(self):
        print("Method in ParentA")

# Define the ParentB class
class ParentB:
    # Method 'method' in ParentB
    def method(self):
        print("Method in ParentB")

# Define the Child class that inherits from ParentA and ParentB
class Child(ParentA, ParentB):
    # Method 'call_parents' in Child
    def call_parents(self):
        # Call the 'method' of ParentA using super(ParentA, self).method()
        super(ParentA, self).method()
        # Call the 'method' of ParentB using super(ParentB, self).method()
        super(ParentB, self).method()

# Create an instance of Child
child_obj = Child()

# Call the 'call_parents' method of the Child class
child_obj.call_parents()


##########################################
# class kazkas:
#     def __init__(self):
#         self.num_kazkur = "vilnius"
#
#     def kaimas(self):
#         self.pav = 'Vilnius'
#         print("Trakai")
#
# # "kazkur" inherits "kazkas" functions, need to use "super()" method
# class kazkur(kazkas):
#     def __init__(self):
#         super().__init__()
#
#     def kaimas(self):
#         # inherits "kazkas" class function "kaimas" with using super().kaimas() and adds "print("Vilkaviskis")"
#         super().kaimas()
#         print("Vilkaviskis")
#
#     def vaziuoja(self):
#         print("Anyksciai")
#
#
# kazkaip = kazkur()
# kazkaip.kaimas()
# kazkaip.vaziuoja()
