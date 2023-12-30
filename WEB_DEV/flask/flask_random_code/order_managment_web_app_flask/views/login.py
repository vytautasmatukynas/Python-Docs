from flask import render_template, redirect, url_for, flash, request, session, Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


login_bp = Blueprint('login_bp', __name__)

# users DB data should be here, change this with users DB
acc = {'username': "admin",
       'password': "pass"}


class LoginForm(FlaskForm):
    user = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Login")


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page. Checks username and if username is valid then store user info
    to session and redirect to index page."""

    form = LoginForm()

    if form.validate_on_submit():
        if form.user.data == acc["username"] and form.password.data == acc["password"]:
            # create session for user
            session['user'] = form.user.data
            return redirect(url_for('main_table.order_table'))
        else:
            flash("Username or password in incorrect. Please try again.")
            return redirect(request.url)

    return render_template('login_page/login.html', form=form)
