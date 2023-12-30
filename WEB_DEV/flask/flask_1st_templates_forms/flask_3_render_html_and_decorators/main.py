from flask import Flask

app = Flask(__name__)

# # Rendering html
# @app.py.route("/")
# def hello_world():
#     return "<p><em><strong>Hello, World!</strong></em></p>" \

# Using python decorators
def bold_decorator(function):
    def bold():
        return f"<strong>{function()}</strong>"
    return bold

def italic_decorator(function):
    def italic():
        return f"<em>{function()}</em>"
    return italic

def underlined_decorator(function):
    def underline():
        return f"<u>{function()}</u>"
    return underline

@app.route("/")
@bold_decorator
def hello_world():
    return "Hello, World!"

@app.route("/a")
@italic_decorator
@underlined_decorator
def hello_world_1():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)