from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



# __file__ -> bcrypt.py, dirname is folder where my file is and abspath is full path
# This line is same as d:/Python/python-default/flask/flask_2nd/flask_6_flask-sqlalchemy/bcrypt.py
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# DB configuration
# Sets up DB location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# Doesnt track every modification of DB. Maybe later.... SOME DAY... ;D
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup our app.py DB
db = SQLAlchemy(app)

# with migrate you can edit SQL table, like adding new column
Migrate(app, db)

# Create db table
class SampleTable(db.Model):
    # Manual table name change. SQLAlchemy take class name and creates table name
    # so you can change table name with this line.
    __tablename__ = 'sample_db'

    # Create columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    age = db.Column(db.Integer)
    count = db.Column(db.Text)

    def __init__(self, name, age, count):
        self.name = name
        self.age = age
        self.count = count
        
    def __repr__(self):
        return f"name: {self.name}, age: {self.age}, count:{self.count}"
    

