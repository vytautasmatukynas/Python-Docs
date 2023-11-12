from abc import ABC, abstractmethod

# Define an abstract class
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

# Create a concrete subclass of the abstract class
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Try to create an instance of the abstract class (will raise an error)
# shape = Shape()  # This will raise a TypeError

# Create an instance of the concrete subclass
circle = Circle(5)
print("Circle Area:", circle.area())
print("Circle Perimeter:", circle.perimeter())
