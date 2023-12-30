from flask import Blueprint, render_template, request, redirect
from datetime import datetime, date
from flask_login import login_required
from project.models import PostModel


main = Blueprint('main', __name__)

year = datetime.now().year
post_date = date.today()


@main.route('/')
def home():
    """ gets all post of all users and show 5 posts per page """

    header_text = "All Posts"

    page = request.args.get('page', 1, type=int)

    blog_posts = PostModel.query.order_by(PostModel.post_date.asc()) \
                                            .paginate(page=page, 
                                                        per_page=5, 
                                                        error_out=False)

    return render_template("index.html", blog_posts=blog_posts, 
                                            year=year, 
                                            header_text=header_text, 
                                            page_name="all posts")


@main.route('/my_posts/<int:current_user>')
@login_required
def user_posts(current_user):
    """ gets all post of all users """

    header_text = "Your Posts"

    blog_posts = PostModel.query.filter_by(user_id=current_user) \
                                            .order_by(PostModel.post_date.asc()) \
                                            .all()

    return render_template("index.html", blog_posts=blog_posts, 
                                            year=year, 
                                            header_text=header_text, 
                                            page_name="user posts")


@main.route('/post/<int:index>')
def post_selected(index):
    """ opens selected post, if you are current_user=true then you will see 
    update/delete buttons, else just read-only post """

    blog_posts = PostModel.query.get(index)

    return render_template("post_pages/post.html", blog_posts=blog_posts, 
                                                    year=year)


@main.route('/search', methods=['GET', 'POST'])
def post_search():
    """ case-insensitive search with wildcards,
    '|' symbol represents the operation 'OR' """

    search_value = request.form.get("search")

    header_text = f"Search result: {search_value}"

    if request.method == 'POST':
        blog_posts = PostModel.query.filter((PostModel.title.ilike(f'%{search_value}%')) |
                                            (PostModel.subtitle.ilike(f'%{search_value}%')) |
                                            (PostModel.text.ilike(f'%{search_value}%'))) \
                                            .order_by(PostModel.post_date.asc()) \
                                            .all()

        return render_template("index.html", blog_posts=blog_posts, 
                                                year=year, 
                                                header_text=header_text)

    else:
        return redirect(request.url)
