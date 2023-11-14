# collects keyword arguments and puts in dict "**"
def named(**kwargs):
    print(kwargs)

named(name='bob', gre=15)

# unpack dict
dict = {'name': 'bob', 'age': 15}

named(**dict)


def print_sample(**kwargs):
    named(**kwargs)
    for arg, value in kwargs.items():
        print(f'{arg}, {value}')

print_sample(name="bob", age=35)