# "name: str" this is saying that "name" should be string
# "-> str" this is saying that this function returns string
def greeting(name: str) -> str:
    return 'Hello ' + name

print(greeting("ooooo"))


# Sample of using hints with Class
class bilekas:
    TIPAS = ('betkas', "betkur")

    def __init__(self, vardas: str, tipas: str, numeris: int):
        self.vardas = vardas
        self.tipas = tipas
        self.numeris = numeris

    # this func returns string "-> str"
    def __repr__(self) -> str:
        return f"{self.vardas}, {self.tipas}, {self.numeris}"

    @classmethod
    # '-> "bilekas"' this method returns "bilekas" object
    def betkas(cls, vardas: str, numeris: int) -> "bilekas":
        return bilekas(vardas, bilekas.TIPAS[0], numeris)
        # <OR>
        # return cls(vardas, cls.TIPAS[0], numeris)

    @classmethod
    def betkur(cls, vardas: str, numeris: int) -> "bilekas":
        return bilekas(vardas, bilekas.TIPAS[1], numeris)
        # <OR>
        # return cls(vardas, cls.TIPAS[0], numeris)


betkas_ = bilekas.betkas("ooo", 5)
print(betkas_)

betkur_ = bilekas.betkur("ooo", 5)
print(betkur_)