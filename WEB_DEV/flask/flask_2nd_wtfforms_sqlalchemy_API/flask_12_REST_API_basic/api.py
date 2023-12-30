from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)

# API call
api = Api(app)

# This could be DB
puppies = [{'name': 'Rufus'}]

class PuppyNames(Resource):

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

    def get(self):
        # gets all elements in API
        return {'puppies': puppies}
    
    
api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(allnames, "/puppies")


if __name__ == '__main__':
    app.run(debug=True)
 