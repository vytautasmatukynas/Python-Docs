from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField, TextAreaField, SelectField,
                     SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

# create secret key
app.config['SECRET_KEY'] = 'THIS IS YOUR SECRET KEY'

class InfoForm(FlaskForm):
    # validators=[DataRequired() this validtors tells that you have to put something in input field to submit it
    label_input_entry = StringField("How are you?", validators=[DataRequired()])
    bool_field = BooleanField("Are you okay?")
    # first one is value, second label
    radio_field = RadioField("Please select anwser:",
                             choices=[('yes', 'i am ok'),
                                      ('no', 'i am f..kd')]
                             )
    # "u" before the string makes string a unit code string, on some OS you need it
    # choice first element is for back end to see and user sees second element
    select_field = SelectField(u'Pick something:',
                               choices=[('oooo', 'ooooommmm'),
                                        ('aaaa', 'aaaaammmmm')]
                               )
    text_area = TextAreaField()
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    """bottom return is index page rendering and if statment return
    grabs data on submition and redirects to thankyou page on
    valid submition"""
    form = InfoForm()
    if form.validate_on_submit():
        # session object is treated like dict
        session['label_input_entry'] = form.label_input_entry.data
        session['bool_field'] = form.bool_field.data
        session['radio_field'] = form.radio_field.data
        session['select_field'] = form.select_field.data
        session['text_area'] = form.text_area.data

        # you can use url_for with redirect in python code, that
        # html template would be cleaner
        return redirect(url_for('thankyou'))

    return render_template('index.html', form=form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == "__main__":
    app.run(debug=True)