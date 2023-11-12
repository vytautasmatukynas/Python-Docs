class Animal:
    def speak(self):
        print("Animal speaks")

class Dog(Animal):
    def speak(self):
        print("Dog barks")

class Cat(Animal):
    def speak(self):
        print("Cat meows")

# Create instances of the subclasses
dog = Dog()
cat = Cat()

# Call the speak method on instances
dog.speak()  # Output: Dog barks
cat.speak()  # Output: Cat meows
