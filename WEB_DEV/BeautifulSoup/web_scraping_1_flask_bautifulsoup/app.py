from flask import Flask, render_template
from scraping.top_250 import topClass
from scraping.moviemeter import meterClass

app = Flask(__name__)


@app.route('/')
@app.route('/top100-popular')
def moviemeter():
    data = meterClass().data()
    title = "Top 100 Most Popular Movies"
    return render_template("moviemeter.html", data=data, title=title)


@app.route('/top250-all-times')
def top250():
    data = topClass().data()
    title = "Top 250 of All Time Movies"
    return render_template("top_250.html", data=data, title=title)


if __name__ == "__main__":
    app.run(debug=True)
