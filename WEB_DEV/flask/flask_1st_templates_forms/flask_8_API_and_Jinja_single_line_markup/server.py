import requests
from flask import Flask, render_template

# HTML File: {{ }} elements inside Jinja markup for single line Python expressions.
# gets data from Python code.
app = Flask(__name__)


@app.route("/<name>")
def main_func(name):
    """ Add data from API. """
    response = requests.get(f'https://api.agify.io?name={name}')
    data = response.json()
    user_age = data['age']

    return render_template("index_blog.html", user=name, age=user_age)


if __name__ == "__main__":
    app.run(debug=True)
