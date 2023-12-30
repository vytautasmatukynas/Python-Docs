from flask import Flask

app = Flask(__name__)

print(__name__)

# URL to open when server is on http://127.0.0.1:5000/
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# URL to open when server is on http://127.0.0.1:5000/aaa
@app.route("/aaa")
def bye_world():
    return "<h1>Bye, World!</h1>"

# run in terminal: flask --app.py flask/flask_1_start/bcrypt.py run
# "app.py.run()" this command runs app.py and you don't need to type anything in command line

if __name__ == "__main__":
    app.run()