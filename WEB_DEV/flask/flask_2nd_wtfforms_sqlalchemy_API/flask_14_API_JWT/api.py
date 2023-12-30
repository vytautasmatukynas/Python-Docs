from flask import Flask
from flask_restful import Resource, Api
from check import auth, identity
from flask_jwt import JWT, jwt_required


# In POSTMAN you will get error with this code, you have to generate
# TOKEN to connect to func that has @jwt_required().
# http://127.0.0.1:5000/auth URL needs to be with 'auth' end, this is default JWT.
# Select POST.
# Click 'Headers' then fill form with 'Key=Content-Type' and 'Value=application/json'.
# Click 'Body'. Select "raw", body is JSON, like python dict. Write in json:
# {"username": "Jonas",
# "password": "pass"}
# Then click SEND and this will generate TOKEN if your username and pass is correct.
# Then go to API url you want and in 'Headers' 'Key=Authorization' and 'Value=JWT YOUR_TOKEN'.
# If everything is ok, then you will get access to API.

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my key'

# API call
api = Api(app)

# JWT call. Need to set up auth and identity func
jwt = JWT(app, auth, identity)

# This could be DB
puppies = [{'name': 'Rufus'}]


class PuppyNames(Resource):

    # with this decoratpr you an GET just if you have auth
    @jwt_required()
    # main methods here is get/post/delete
    def get(self, name):
        for pup in puppies:
            if pup['name'] == name:
                return pup

        # return None if name isn't in the list and send back status 404
        return {'name': None}, 404

    def post(self, name):
        # add new value to API
        pup = {'name': name}

        puppies.append(pup)

        return pup

    def delete(self, name):
        # delete element from API
        for index, pup in enumerate(puppies):
            if pup['name'] == name:
                puppies.pop(index)
                return {'note': 'delete success'}


class allnames(Resource):
    @jwt_required()
    def get(self):
        # gets all elements in API
        return {'puppies': puppies}


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(allnames, "/puppies")

if __name__ == '__main__':
    app.run(debug=True)