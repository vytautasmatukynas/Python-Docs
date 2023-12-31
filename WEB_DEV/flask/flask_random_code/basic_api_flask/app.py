from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api
import os

from user_config import auth, identity

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWT(app, auth, identity)


class ItemDB(db.Model):
    __tablename__ = "item_db"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    product = db.Column(db.String(100), nullable=False)

    def __init__(self, name, product):
        self.name = name
        self.product = product


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "product")


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class get_items(Resource):

    def get(self):
        show_names = request.args.get("names", type=bool, default=False)
        show_products = request.args.get("products", type=bool, default=False)

        items = ItemDB.query.all()

        if items:
            try:
                if show_names and show_products:
                    result = [{"name": item.name, "product": item.product}
                              for item in items]
                    return result, 200

                elif show_names:
                    result = [{"name": item.name} for item in items]
                    return result, 200

                elif show_products:
                    result = [{"product": item.product} for item in items]
                    return result, 200

                else:
                    result = items_schema.dump(items)
                    return result, 200

            except SQLAlchemyError as e:
                return abort(500, {"error": "Database error: " + str(e)})

        else:
            return {"message": "No items found"}, 404


class get_item(Resource):

    def get(self, item_id):
        show_names = request.args.get("name", type=bool, default=False)
        show_products = request.args.get("product", type=bool, default=False)

        item = ItemDB.query.get(item_id)

        if item:
            try:
                if show_names and show_products:
                    result = [{"name": item.name, "product": item.product}]
                    return result, 200

                elif show_names:
                    result = [{"name": item.name}]
                    return result, 200

                elif show_products:
                    result = [{"product": item.product}]
                    return result, 200

                else:
                    result = item_schema.dump(item)
                    return result, 200

            except SQLAlchemyError as e:
                return abort(500, {"error": "Database error: " + str(e)})

        else:
            return {"message": "No item found"}, 404


class create_item(Resource):

    @jwt_required()
    def post(self):
        try:
            name = request.args.get("name") or ""
            product = request.args.get("product") or ""

            new_item = ItemDB(name=name, product=product)
            db.session.add(new_item)
            db.session.commit()

            return item_schema.dump(new_item), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": "Database error: " + str(e)}, 500


class update_item(Resource):

    @jwt_required()
    def put(self, item_id):
        item = ItemDB.query.get(item_id)

        if item:
            try:
                new_name = request.args.get("name") or item.name
                new_product = request.args.get("product") or item.product

                item.name = new_name
                item.product = new_product
                db.session.commit()

                return item_schema.dump(item), 200

            except SQLAlchemyError as e:
                db.session.rollback()
                return {"error": "Database error: " + str(e)}, 500

        else:
            return {"error": "Item not found"}, 404


class delete_item(Resource):

    @jwt_required()
    def delete(self, item_id):
        item = ItemDB.query.get(item_id)

        if item:
            try:
                db.session.delete(item)
                db.session.commit()

                return {"message": "Item deleted"}, 200

            except SQLAlchemyError as e:
                db.session.rollback()
                return {"error": "Database error: " + str(e)}, 500
        else:
            return {"error": "Item not found"}, 404


api.add_resource(get_items, "/items")
api.add_resource(get_item, "/item//<int:item_id>")
api.add_resource(create_item, "/item_add")
api.add_resource(update_item, "/item_update/<int:item_id>")
api.add_resource(delete_item, "/item_delete/<int:item_id>")


if __name__ == "__main__":
    app.run(debug=True)
