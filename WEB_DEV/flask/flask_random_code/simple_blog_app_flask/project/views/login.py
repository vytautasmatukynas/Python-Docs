from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash
from datetime import datetime, date

from project.models import UserModel
from project.forms import LoginForm


log = Blueprint('log', __name__)

year = datetime.now().year
post_date = date.today()


@log.route("/login", methods=['GET', 'POST'])
def login():
    """ login user, if there is no sush user then you will be 
    redirected to register page """
    
    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = UserModel.query.filter_by(user=form.user.data).first()
            password = check_password_hash(user.password, form.password.data)
            if password == True and user is not None:
                login_user(user)
                
                flash(f"User:'{user.user}' - logged in.")
                return redirect(url_for('main.home'))
            
        except AttributeError:
                flash(f"There is no - username:'{form.user.data}'. Please register username.")
                return redirect(url_for('user.register_user'))
            
    return render_template('user_pages/login.html', form=form, year=year)


@log.route('/logout')
@login_required
def logout():
    """ logout user and redirect to home page"""
    
    logout_user()
    
    flash(f"Logged out.")
    return redirect(url_for('main.home'))