from flask_sqlalchemy import SQLAlchemy

# crete sql object
db = SQLAlchemy()

class StoreModel(db.Model):
    # sql table name
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    # if 'unique=True' is false, you can have multiple items with same name
    # 'nullable=False' is same as 'NOT NULL'
    name = db.Column(db.String(80), unique=True, nullable=False)
    # create relationship between ItemModel and StoreModel
    # back_populates="store" relationship variable name in ItemModel
    items = db.relationship("ItemModel", back_populates="store", lazy='dynamic')