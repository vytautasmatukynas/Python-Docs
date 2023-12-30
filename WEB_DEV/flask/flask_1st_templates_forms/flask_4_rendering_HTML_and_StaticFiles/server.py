from flask import Flask
from flask import render_template


app = Flask(__name__)




@app.route("/")
def main_func():
    # renders html file to browser. HTML file should be in core folder
    # and all img/css_files/ico and etc. should be in static folder.
    # That is default folders for flask apps.
    return render_template("index_blog.html")




if __name__ == "__main__":
    app.run(debug=True)