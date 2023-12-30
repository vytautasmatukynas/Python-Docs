import random
from datetime import datetime

from flask import Flask, render_template

# HTML File: {{ }} elements inside Jinja markup for single line Python expressions.
# gets data from Python code.

app = Flask(__name__)


@app.route("/")
def main_func():
    """ Can add as many variables as you want, second param in render_templates
    acts as **kwargs, so you have just to type key=value you want.
    In this example it's random number generator and datetime generator.
    Check HTML file too."""
    random_number = random.randint(0, 50)
    datetime_year = datetime.now().year
    return render_template("index_blog.html", num=random_number, date=datetime_year)


if __name__ == "__main__":
    app.run(debug=True)
