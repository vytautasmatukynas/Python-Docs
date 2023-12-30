import requests
import random
from datetime import datetime
from flask import Flask, render_template

# HTML File: {{ }} elements inside Jinja markup for single line Python expressions.
# gets data from Python code.

# HTMl File: {% %} elements inside Jinja multiline statement markup. Can use Python code
# inside this kind of markup. Have to add markup for each line of Python code.
# {% endfor %} end for loop. {% endif %} end if statement.

# HTML File: <a href="{{ url_for('blog_func') }}">GO TO BLOG</a> create <a> with href that
# is linked to python function. Function name must be in '' "" like string.
# This method will generate a hyperlink that will take you to route that function is.
# You can pass keyword argument <a href="{{ url_for('blog_func', num=3) }}">GO TO BLOG</a> and this
# will open link 'http://127.0.0.1:5000/blog/3', with value you passed in params.

app = Flask(__name__)

@app.route("/")
def main_func():
    """ Can add as many variables as you want, second param in render_templates
    acts as **kwargs, so you have just to type key=value you want.
    In this example it's random number generator and datetime generator.
    Check HTML file too."""
    random_number = random.randint(0, 50)
    datetime_year = datetime.now().year
    return render_template("base.html", num=random_number, date=datetime_year)


@app.route("/blog/<num>")
def blog_func(num):
    """ Add data from API.
    Pass in key word argument num as param. """
    print(num)
    response = requests.get('https://api.npoint.io/362a61befce3d173e925')
    blog_posts = response.json()
    print(blog_posts)

    return render_template("index_blog.html", post_data=blog_posts)


if __name__ == "__main__":
    app.run(debug=True)