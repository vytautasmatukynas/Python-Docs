# Basic Python Decorator Functions
def sample(funkcija):
    def sample1():
        print("kazkas 1")
        funkcija()
        print("kazkas 2")

    return sample1

@sample
def sample2():
    print("kazkas 3")

sample2()

# Advanced Python Decorator Functions
class User:
    def __init__(self, name):
        self.name = name
        self.is_logged_in = False

def is_authenticated_decorator(function):
    def wrapper(*args, **kwargs):
        if args[0].is_logged_in == True:
            function(args[0])
    return wrapper

@is_authenticated_decorator
def create_blog_post(user):
    print(f"This is {user.name}'s new blog post.")

new_user = User("Kazkas")
new_user.is_logged_in = True
create_blog_post(new_user)


