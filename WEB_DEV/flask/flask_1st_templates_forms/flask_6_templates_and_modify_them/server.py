from flask import Flask, render_template

"""You can edit template in browser, type in 'Console' - 'document.body.contentEditable=true' 
to enable editing in browser and you can edit live in browser. 
Or delete elements by clicking on them in 'Elements' and after you finish, dont click refresh, 
first download your new HTML file and replace it with your old HTML file"""

app = Flask(__name__)

@app.route("/")
def main_func():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)