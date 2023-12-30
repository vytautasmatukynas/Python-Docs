from datetime import datetime, date

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os


############################## SETUP APP ##########################
# create flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
# set upload folder dir
app.config['UPLOAD_FOLDER'] = "/static/img/"
# database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

# get current year
year = datetime.now().year
post_date = date.today()

# setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
##########################################################################

########################## BLUEPRINTS #####################################
from project.views.errors import errors
from project.views.login import log
from project.views.user import user
from project.views.posts import posts
from project.views.main import main

app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(user)
app.register_blueprint(log)
app.register_blueprint(errors)
################################################################################
