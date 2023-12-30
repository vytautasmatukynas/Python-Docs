from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from datetime import timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'THIS IS YOUR SECRET KEY'
# Sessions have a temporary lifetime and are usually cleared after a period of 
# inactivity or when the user closes their browser.
# Session data is typically stored on the server-side, which allows for larger data storage.
# Session lifetime change. Session will be deleted after 60 seconds of inactivity.
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=60) 

# users DB should be here
acc = {'username': "admin",
       'password': "pass"}

class LoginForm(FlaskForm):
    user = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Login")


@app.route('/')
def index():
    """ If session is True then log user. 
    If session is False then redirect to login page."""
    
    if 'user' in session:
        return "<h1>Logged In!</h1>"
    else:
        return redirect(url_for('login'))

@app.route('/register')
def register():
    return "<h1>Registration</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page. Checks username and if username is valid then store user info
    to session and redirect to index page."""
    
    form = LoginForm()
    
    if form.validate_on_submit():
        if form.user.data == acc["username"] and form.password.data == acc["password"]:
            session['user'] = form.user.data
            return redirect(url_for('index'))
        else:
            flash("Username or password in incorrect. Please try again.")
            return redirect(request.url)
        
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 