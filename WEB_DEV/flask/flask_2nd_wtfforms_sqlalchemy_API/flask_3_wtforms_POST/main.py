from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

# create secret key
app.config['SECRET_KEY'] = 'THIS IS YOUR SECRET KEY'

# create flask form
class InfoForm(FlaskForm):

    # label and input
    sample = StringField("How are you?")
    # submit button
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # sample is False that you could use it in "if"
    sample = False

    # import "form" class
    form = InfoForm()

    # if form is valid
    if form.validate_on_submit():
        # get data from form
        sample = form.sample.data
        # reset form
        form.sample.data = ''

    return render_template('index.html', sample=sample, form=form)

if __name__ == "__main__":
    app.run(debug=True)