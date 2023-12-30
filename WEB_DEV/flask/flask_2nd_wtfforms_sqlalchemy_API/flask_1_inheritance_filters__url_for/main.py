from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/<name>')
def second_page(name):
    return render_template('signed.html', name=name)

if __name__ == "__main__":
    app.run(debug=True)