from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'  # SQLite database for simplicity
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Define a sample database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

# Initialize Flask-Admin
admin = Admin(app)

# Create a ModelView for the User model
class UserAdmin(ModelView):
    column_list = ('id', 'username', 'email')  # Specify columns to display

# Add the User model to the admin interface
admin.add_view(UserAdmin(User, db.session))

if __name__ == '__main__':
    db.create_all()  # Create the database tables
    app.run(debug=True)
