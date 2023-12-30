from user import User

users = [User(1, 'Jonas', "pass"),
         User(1, 'Janina', "pass123")]


username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def auth(username, password):
    # check if user exists and return user
    # username_table['username'] would work, but if there is no user it would get an error
    user = username_table.get(username, None)
    if user and password == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
