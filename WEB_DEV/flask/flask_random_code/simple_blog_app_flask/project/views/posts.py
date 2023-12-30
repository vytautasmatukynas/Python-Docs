from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from datetime import datetime, date
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
import random
import string


from project.models import PostModel
from project.forms import AddUpdatePostForm
from project import db, app


posts = Blueprint('posts', __name__)

year = datetime.now().year
post_date = date.today()



def generate_random_string(length):
    """ create random string combination """

    characters = string.ascii_uppercase + string.digits + string.ascii_lowercase
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string


@posts.route("/add", methods=['GET', 'POST'])
@login_required
def post_add():
    """ adds new post if user is logged in """

    form = AddUpdatePostForm()
    
    random_number = generate_random_string(20)

    try:
        if form.validate_on_submit():
            file = form.image.data

            if file != "" and file is not None:
                # Save the file - "current_dir, folder_to_upload, random string, filename"
                file.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                          + app.config['UPLOAD_FOLDER']
                          + f"{random_number}"
                          + secure_filename(file.filename))

                image = f"{random_number}" + \
                    secure_filename(form.image.data.filename)
            else:
                image = "no_image.jpg"

            new_post = PostModel(
                title=form.title.data,
                subtitle=form.subtitle.data,
                text=form.text.data,
                post_date=f"{post_date} by {current_user.user}",
                user_id=current_user.id,
                image=image
            )

            db.session.add(new_post)
            db.session.commit()

            flash(f"Post:'{form.title.data}' was created.")
            return redirect(url_for('main.home'))

    except IntegrityError:
        flash(
            f"'{form.title.data}' - this title exists, please select diffrent title.")
        return redirect(request.url)

    return render_template('post_pages/add_post.html', form=form,
                                                        year=year)


@posts.route("/update/<int:index>", methods=['GET', 'POST'])
@login_required
def post_update(index):
    """ updates post if current_user is logged in, else this won't work, you 
    won't see update button in post page """

    form = AddUpdatePostForm()

    blog_posts = PostModel.query.get(index)

    # First grab the file
    random_number = generate_random_string(20)

    if blog_posts.author != current_user:
        abort(403)

    if form.validate_on_submit():
        try:
            file = form.image.data

            blog_posts.title = form.title.data
            blog_posts.subtitle = form.subtitle.data
            blog_posts.text = form.text.data
            blog_posts.post_date = f"{post_date} by {current_user.user}"

            if file != "" and file is not None:
                # Save the file - "current_dir, folder_to_upload, filename" and database
                file.save(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                          + app.config['UPLOAD_FOLDER']
                          + f"{str(random_number)}"
                          + secure_filename(file.filename))

                blog_posts.image = f"{str(random_number)}" + \
                                        secure_filename(file.filename)

            db.session.commit()

            flash(f"Post:'{blog_posts.title}' was updated.")
            return redirect(url_for('main.home'))

        except IntegrityError:
            flash(
                f"'{form.title.data}' - this title exists, please select diffrent title.")
            return redirect(request.url)

    if request.method == "GET":

        form.title.data = blog_posts.title
        form.subtitle.data = blog_posts.subtitle
        form.text.data = blog_posts.text

        return render_template('post_pages/update_post.html', form=form,
                                                                year=year)


@posts.route("/delete/<int:index>", methods=['GET', 'POST'])
@login_required
def delete_post(index):
    """ deletes post if current_user is logged in, else this won't work, you 
    won't see delete button in post page """

    blog_posts = PostModel.query.get(index)

    if blog_posts.author != current_user:
        abort(403)

    db.session.delete(blog_posts)
    db.session.commit()

    flash(f"Post:'{blog_posts.title}' was deleted.")
    return redirect(url_for('main.home'))
