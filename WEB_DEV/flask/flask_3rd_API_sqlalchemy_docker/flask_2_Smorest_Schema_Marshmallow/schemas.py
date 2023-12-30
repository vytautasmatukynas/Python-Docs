from marshmallow import Schema, fields

# marshmallow can turn dict and object in to json.

class ItemSchema(Schema):
    # 'dump_only=True' only returns data
    # 'required=True' you can return and send data
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

    # same as this:
    # item_schema_dict = {
    #     'id': fields.Str(dump_only=True),
    #     'name': fields.Str(required=True),
    #     'price': fields.Float(required=True),
    #     'store_id': fields.Str(required=True)
    # }


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
