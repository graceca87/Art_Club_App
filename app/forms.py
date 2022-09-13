from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, EqualTo
from flask_wtf.file import FileField, FileAllowed



class CommentForm(FlaskForm):
    body = StringField('Body', validators=[InputRequired()])
    submit = SubmitField()


class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class ImageForm(FlaskForm):
    file = FileField('File', validators=[
        FileAllowed(['jpg','jpeg','png'], "We only accenpt JPG or PNG images")
    ])
    title = StringField('Title', [
        validators.InputRequired(),
        validators.Length(max=200)
    ])
    comments = TextAreaField('Comments')
    submit = SubmitField('Submit')