# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Create a Flask web application
app = Flask(__name__)

# Secret key for session management (replace with a strong secret in production)
app.secret_key = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# User class for user management (replace this with a database model in production)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Simulated user database (replace with a real database in production)
users = {'user1': {'password': 'password1'}, 'user2': {'password': 'password2'}}

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)

        if user and user['password'] == password:
            user_obj = User(username)
            login_user(user_obj)
            flash('Login successful', 'success')
            return redirect(url_for('protected'))
        else:
            flash('Login failed. Please check your credentials.', 'error')

    return render_template('login.html')

# Route for the protected page (requires authentication)
@app.route('/protected')
@login_required
def protected():
    return f'Hello, {current_user.id}! This is a protected page. <a href="/logout">Logout</a>'

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
