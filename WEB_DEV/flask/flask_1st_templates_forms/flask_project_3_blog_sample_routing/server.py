from datetime import datetime

import requests
from flask import Flask, render_template

app = Flask(__name__)

year = datetime.now().year
# print(year)
response = requests.get('https://api.npoint.io/362a61befce3d173e925')
blog_posts = response.json()


# print(blog_posts)

@app.route('/')
def home():
    return render_template("index.html", post_data=blog_posts, date=year)


@app.route('/post/<int:index>')
def post_selected(index):
    post_current = None
    for post in blog_posts:
        if post['id'] == index:
            post_current = post

    return render_template("post.html", post_data=post_current, date=year)


if __name__ == "__main__":
    app.run(debug=True)
