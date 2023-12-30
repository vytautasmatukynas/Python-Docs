from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup')
def sign_form():
    return render_template('signup.html')

@app.route('/signed')
def signed_page():
    # grab info from form:
    name = request.args.get('first')
    second_name = request.args.get('second')

    return render_template('signed.html', name=name, second_name=second_name)

# error page. 404 WEB not found error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)