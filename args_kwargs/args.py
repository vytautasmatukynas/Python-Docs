# collects multiple arguments with "*", returns tuple
def multiply(*args):
    return args, args[0], args[2]

print(multiply(1, 5, 6))

def multiply(*args):
    for arg in args:
        x = arg * 10
        return x

print(multiply(11, 12, 13))

# extract tuples list set with "*"
def add(x, y):
    return x + y

nums = [1, 5]
print(add(*nums))

nums = (1, 5)
print(add(*nums))

nums = {1, 7}
print(add(*nums))

# using operators with args. Collect all arguments to tuple and have named argument at the end "operator"
def apply(*args, operator):
    if operator == "*":
        return multiply(*args)
    elif operator == '+':
        return sum(args)
    else:
        return 'No operator'

print(apply(1, 5, 7, operator="+"))
print(apply(1, 5, 7, operator="*"))
