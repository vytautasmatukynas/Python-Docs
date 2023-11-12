# CLASS INHERITANCE
class Sample_1:
    def __init__(self, sample_Sample_1):
        self.sample_Sample_1 = sample_Sample_1

    def __str__(self):
        return f"{self.sample_Sample_1}"

result_1 = Sample_1("AAAA")
print(result_1)


class Sample_2(Sample_1):
    def __init__(self, sample_Sample_1):
        # inherits sample_Sample_1 from Sample_1 class __init__ func
        super().__init__(sample_Sample_1)

    def __str__(self):
        return f"O: {self.sample_Sample_1}"

result_2 = Sample_2("OOOOO")
print(result_2)


# CLASS COMPOSITION
class Sample_1:
    def __init__(self, *sample_Sample_1):
        self.sample_Sample_1 = sample_Sample_1

    def __str__(self):
        return f"{self.sample_Sample_1}, {len(self.sample_Sample_1)}"

result = Sample_1("AAAA")
print(result_1)


class Sample_2:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"O: {self.name}"

result_1 = Sample_2("AAAAAA")
result_2 = Sample_2("OOOOOO")
result_sum = Sample_1(Sample_2, Sample_2)
print(result_sum)

