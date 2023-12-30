import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from schemas import ItemSchema, ItemUpdateSchema
from db import items

blp = Blueprint("Items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):

    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, "Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, "Item not found.")

    # 'item_data' can be any name, it just has to be second param, goes after 'self'.
    # this second param will contain json, same as "request.get_json()".
    # 'item_data' goes to ItemSchema form, checks if everything is valid and then gives
    # method argument "@blp.arguments(ItemUpdateSchema)" that this is valid dict.
    # basically this checks if your data is valid.
    @blp.arguments(ItemUpdateSchema)
    # main success response decorator. It will pass whatever we return throw Schema form.
    # if response is false, like ID doesn't exist, then it will raise exception
    # and abort.
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]

            # https://blog.teclado.com/python-dictionary-merge-update-operators/
            # same as 'items[item_id]=item_data'
            item |= item_data

            return item

        except KeyError:
            abort(404, "Item not found.")


@blp.route("/item")
class ItemList(MethodView):
    # 'many=True' can get multiple arguments. All values will be turned in to a list.
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, f"Item already exists.")

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item

        return item
