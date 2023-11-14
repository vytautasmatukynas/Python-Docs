# collects arguments to tuple and if keyword arguments then collects it to dict
# this function accepts unlimited arguments and keyword arguments
def both(*args, **kwargs):
    print(args)
    print(kwargs)

both(1, 5, 'kazkas', name='bob')