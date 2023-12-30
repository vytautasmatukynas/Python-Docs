from flask import Flask

app = Flask(__name__)

# imitation of DB ir JSON or whatever you will use
stores = [{"name": "store1", "items": [{"name": "Chair", "price": 15.99}]}]

# app.py.get('/') same as app.py.route('/', methods=['GET']
# app.py.post('/') same as app.py.route('/', methods=['POST']
@app.get("/stores")
def get_stores():
    """ get all stores and items """
    return {"stores": stores}


@app.get("/store/<string:name>")
def get_store(name):
    """ get store 'name' """
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404


@app.post("/store/<string:name>")
def create_store(name):
    """ create store 'name' """
    new_store = {"name": f"{name}", "items": []}
    stores.append(new_store)
    return new_store, 201


@app.get("/store/<string:name>/items")
def get_item_in_store(name):
    """ get store 'name' items """
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404


@app.post("/store/<string:name>/<string:item>/<float:price>")
def create_item(name, item, price):
    """ create items at store 'name' """
    for store in stores:
        if store["name"] == name:
            new_item = {"name": f"{item}", "price": f"{price}"}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


# if __name__ == "__main__":
#     app.py.run(debug=True, port=5000)