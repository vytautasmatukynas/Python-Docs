from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class AddUpdatePostForm(FlaskForm):

    title = StringField("Enter Title:", validators=[DataRequired()])
    subtitle = StringField("Enter Subtitle:", validators=[DataRequired()])
    text = TextAreaField("Write Post:")
    image = FileField("Select Image:", validators=[
                      FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField("Post")


class RegisterForm(FlaskForm):

    user = StringField("Enter Username:", validators=[DataRequired()])
    password = PasswordField("Enter Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:", 
                                     validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    user = StringField("Enter Username:", validators=[DataRequired()])
    password = PasswordField("Enter Password:", validators=[DataRequired()])
    submit = SubmitField("Login")


class UpdateUserForm(FlaskForm):

    user = StringField("Enter New Username:", validators=[DataRequired()])
    password = PasswordField("Enter Password:", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password:", 
                                     validators=[DataRequired()])
    submit = SubmitField("Submit")


class UpdatePasswordForm(FlaskForm):

    old_password = PasswordField("Enter Password:", 
                                 validators=[DataRequired()])
    password = PasswordField("Enter New Password:",
                             validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password:", 
                                     validators=[DataRequired()])
    submit = SubmitField("Submit")