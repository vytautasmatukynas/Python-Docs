from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/aaa")
def bye_world():
    return "<h1>Bye</h1>"

# You can add variable sections to a URL by marking sections with <variable_name>.
# Your function then receives the <variable_name> as a keyword argument.
# Optionally, you can use a converter to specify the type of the argument like <converter:variable_name>.

# Convers to string, int, float, path, uuid

# Try typing http://127.0.0.1:5000/username/Sample, it renders dynamicly "kazkas" to web
@app.route("/<name>")
def name_(name):
    return F"{name}"

# creates path "/Sample2"
@app.route("/<path:name>")
def name_2_path(name):
    return F"{name}" + "2"

# creates path "/Sample/1"
@app.route("/<name>/1")
def name_1(name):
    return F"{name}" + "1"

#Creates path "/Sample/Sample_Number"
@app.route("/<path:name>/<int:number>")
def name_3_path(name, number):
    return F"{name}" + f"{number}"



if __name__ == "__main__":
    # debug=True turns on debug mode. Reloads the server after changes in code/file.
    # And debugs code, just error is shown in browser when you load code, not in Run.
    app.run(debug=True)