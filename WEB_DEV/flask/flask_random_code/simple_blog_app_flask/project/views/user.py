from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from project.models import UserModel, PostModel
from project.forms import RegisterForm, UpdateUserForm, UpdatePasswordForm
from project import db


user = Blueprint('user', __name__)

year = datetime.now().year
post_date = date.today()


@user.route("/register", methods=['GET', 'POST'])
def register_user():
    """ register new user and redirect to login page"""

    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data == form.confirm_password.data:
            try:
                new_user = UserModel(
                    user=form.user.data,
                    password=generate_password_hash(form.password.data)
                )

                db.session.add(new_user)
                db.session.commit()

                flash(f"User:'{form.user.data}' registration was successful.")
                return redirect(url_for('log.login'))

            except:
                flash(
                    f"Can't create - username:'{form.user.data}'. Please select different username.")
                return redirect(request.url)

    return render_template('user_pages/register.html', form=form,
                           year=year)


@user.route("/delete/user/<int:current_user>", methods=['POST'])
@login_required
def delete_user(current_user):
    """ delete user if current_user is logged in """

    password = request.form.get('password')

    user_data = UserModel.query.filter_by(id=current_user).first()

    if user_data:
        if check_password_hash(user_data.password, password):
            posts = PostModel.query.filter_by(user_id=user_data.id).all()

            for post in posts:
                db.session.delete(post)

            db.session.delete(user_data)
            db.session.commit()

            logout_user()

            flash(f"User '{user_data.user}' was deleted.")
            return redirect(url_for('main.home'))

        else:
            flash("Password is incorrect.")

    else:
        flash("User not found.")

    return redirect(url_for('main.home'))


@user.route("/edit_username/<int:current_user>", methods=['GET', 'POST'])
@login_required
def edit_username(current_user):
    """ update username if current_user is logged in """

    form = UpdateUserForm()

    user_data = UserModel.query.get(current_user)

    try:
        if form.validate_on_submit() and \
                check_password_hash(user_data.password, form.password.data) == True and \
                check_password_hash(user_data.password, form.confirm_password.data) == True:

            user_data.user = form.user.data

            db.session.commit()

            flash(f"Changed to new username:'{user_data.user}'.")
            return redirect(url_for('main.home'))

        elif form.validate_on_submit() and \
            (check_password_hash(user_data.password, form.password.data) == False or
             check_password_hash(user_data.password, form.confirm_password.data) == False):

            flash(f"Please type correct password for '{user_data.user}'.")
            return redirect(request.url)

        if request.method == "GET":

            form.user.data = user_data.user

            return render_template('user_pages/edit_user.html', form=form,
                                   year=year)

    except:
        flash(
            f"Can't create - username:'{form.user.data}'. Please select different username.")
        # redirect to same page. Basically refresh page.
        return redirect(request.url)


@user.route("/edit_password/<int:current_user>", methods=['GET', 'POST'])
@login_required
def edit_password(current_user):
    """ update password if current_user is logged in """

    form = UpdatePasswordForm()

    user_data = UserModel.query.get(current_user)

    if form.password.data == form.confirm_password.data:

        if form.validate_on_submit() and \
                check_password_hash(user_data.password, form.old_password.data) == True:

            user_data.password = generate_password_hash(form.password.data)

            db.session.commit()

            flash(f"Password was changed.")
            return redirect(url_for('main.home'))

        elif form.validate_on_submit() and \
                check_password_hash(user_data.password, form.old_password.data) == False:
            flash(f"Password you typed is incorrect.")
            return redirect(request.url)

    else:
        flash(f"New password didn't match. Please try again.")
        # redirect to same page. Basically refresh page.
        return redirect(request.url)

    return render_template('user_pages/edit_password.html', form=form,
                           year=year)
