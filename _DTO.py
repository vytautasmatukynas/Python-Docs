class PersonDTO:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f"PersonDTO(name='{self.name}', age={self.age})"

# Creating instances of the PersonDTO class
person1 = PersonDTO("Alice", 30)
person2 = PersonDTO("Bob", 25)

# Accessing attributes
print(person1.name, person1.age)  # Output: Alice 30

# String representation (defined by __repr__)
print(person1)  # Output: PersonDTO(name='Alice', age=30)

# Custom equality comparison (defined by __eq__)
print(person1 == person2)  # Output: False
