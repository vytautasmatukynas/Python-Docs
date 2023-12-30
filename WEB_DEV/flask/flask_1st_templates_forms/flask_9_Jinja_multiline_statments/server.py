import requests
from flask import Flask, render_template

# HTML File: {{ }} elements inside Jinja markup for single line Python expressions.
# gets data from Python code.

# HTMl File: {% %} elements inside Jinja multiline statement markup. Can use Python code
# inside this kind of markup. Have to add markup for each line of Python code.
# {% endfor %} end for loop. {% endif %} end if statement.

app = Flask(__name__)


@app.route("/")
def main_func():
    """ Add data from API. """
    response = requests.get('https://api.npoint.io/362a61befce3d173e925')
    blog_posts = response.json()
    print(blog_posts)

    return render_template("index_blog.html", post_data=blog_posts)


if __name__ == "__main__":
    app.run(debug=True)
