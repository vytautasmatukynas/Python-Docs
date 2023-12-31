class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.id},{self.username},{self.password}"


# users DB data should be here, change this with users DB
users = [User(1, 'admin', "pass")]


username_table = {user.username: user for user in users}
userid_table = {user.id: user for user in users}


def auth(username, password):
    # check if user exists and return user
    user = username_table.get(username, None)
    if user and password == user.password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)