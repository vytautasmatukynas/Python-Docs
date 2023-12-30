import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'db_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

Migrate(app, db)


class Puppy(db.Model):
    __tablename__ = 'puppies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    
    # one2many relantionship
    # connect Puppy to Many Toys
    # toys has relantionship with model Toy
    # 'Toy' is child model and backref='puppy' is parent model "Puppy"
    toys = db.relationship('Toy', backref='puppy', lazy='dynamic')
    
    # one2one relantionship
    # connect puppy to owner
    # uselist creates list of items, if it is set to False then it gets just one Owner
    owner = db.relationship('Owner', backref='puppy', uselist=False)
    
    def __init__(self, name):
        self.name = name
    
    # render output to text(str)
    def __repr__(self):
        if self.owner:
            return f"Name: {self.name} and Owner: {self.owner.name}"    
        else:
            return f"Name: {self.name} no Owner"
        
    def report_toys(self):
        print("Toys:")
        for toy in self.toys:
            print(toy.item_name)
            
    
class Toy(db.Model):
    __tablename__ = 'toys'
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
    
    # The FOREIGN KEY constraint prevents invalid data 
    # from being inserted into the foreign key column, because it has to be 
    # one of the values contained in the parent table.
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, item_name, puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id


class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))
    
    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id
    
