from flask import Flask, render_template, flash, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


app = Flask(__name__)

app.config['SECRET_KEY'] = 'KEY'


class SimpleForm(FlaskForm):
    input_text = StringField('op op op')
    submit = SubmitField("click")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SimpleForm()

    if form.validate_on_submit():
        session['input_text'] = form.input_text.data
        flash(session['input_text'])
        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)