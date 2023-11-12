# Without @classmethod, class with public functions
class bilekas:
    TIPAS = ('betkas', "betkur")

    def __init__(self, vardas, tipas, numeris):
        self.vardas = vardas
        self.tipas = tipas
        self.numeris = numeris

    def __repr__(self):
        return f"{self.vardas}, {self.tipas}, {self.numeris}"

# Have to create variable for class to call it
betkuris = bilekas("ooo", "aaa", 5)
print(betkuris)

# Class methods are methods that are called on the class itself, not on a specific object instance.
# A class method is bound to the class and not the object of the class.
# It can access only class variables.

# With @classmethod function has "cls", like without method has "self" argument

# With @classmethod, class with static function
class bilekas:
    TIPAS = ('betkas', "betkur")

    def __init__(self, vardas, tipas, numeris):
        self.vardas = vardas
        self.tipas = tipas
        self.numeris = numeris

    def __repr__(self):
        return f"{self.vardas}, {self.tipas}, {self.numeris}"

    @classmethod
    def betkas(cls, vardas, numeris):
        return bilekas(vardas, bilekas.TIPAS[0], numeris)
        # <OR>
        # return cls(vardas, cls.TIPAS[0], numeris)

    @classmethod
    def betkur(cls, vardas, numeris):
        return bilekas(vardas, bilekas.TIPAS[1], numeris)
        # <OR>
        # return cls(vardas, cls.TIPAS[0], numeris)

# Calls class directly
print(bilekas.betkas("ooo", 5))
print(bilekas.betkur("ooo", 5))
