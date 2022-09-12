from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length


class AddyForm(FlaskForm):
    first_name = StringField('First Name', validators= [InputRequired()])
    last_name = StringField('Last Name', validators= [InputRequired()])
    phone_number = StringField('Phone Number', validators= [InputRequired(), Length(min=7, max=20)])
    street_address = StringField('Street Address', validators= [InputRequired()])
    city = StringField('City', validators= [InputRequired()])
    state = StringField('State', validators= [InputRequired()])
    country = StringField('Country', validators= [InputRequired()])
    zip_code = StringField('Zip Code', validators= [InputRequired()])
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





