from flask_sqlalchemy import SQLAlchemy

# crete sql object
db = SQLAlchemy()

class ItemModel(db.Model):
    # sql table name
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    # if 'unique=True' is false, you can have multiple items with same name
    # 'nullable=False' is same as 'NOT NULL'
    name = db.Column(db.String(80), unique=True, nullable=False)
    # 'precision=2' tells that float number will have 2 numbers after comma
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    # 'db.ForeignKey("stores.id")' this tells that this column maps to 'stores' table 'id' column
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    # create relationship between ItemModel and StoreModel
    # back_populates="items" relationship variable name in StoreModel
    store = db.relationship("StoreModel", back_populates="items")