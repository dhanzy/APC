import pycountry
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextField, SelectField, SubmitField, PasswordField, IntegerField, StringField, FileField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from flask_security import RegisterForm
import phonenumbers

class LoginForm(FlaskForm):
    username = TextField('Username', validators=[])
    password = PasswordField('Password', validators=[])


class RegisterationForm(FlaskForm):
    firstname = TextField('First Name')
    lastname = TextField('Last Name')
    email = TextField('Email')
    username = TextField('Username')
    password = PasswordField('Password')
    local_government = TextField('Local Government')
    nationality = TextField('Nationality')


class ExtendedRegisterForm(RegisterForm):
    firstname =StringField('First Name', validators=[DataRequired(), Length(max=32)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=32)])
    phone = StringField('Phone', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male','Male'), ('female','Female')])
    country = SelectField('Country Of Residence', choices=[(country.name, country.name) for country in pycountry.countries])
    state = SelectField('State', choices=[('Lagos','Lagos'),('Ekiti','Ekiti'),('Enugu','Enugu'),('Gombe','Gombe')])
    city = StringField('City', validators=[DataRequired(), Length(max=30)])
    lga = StringField('Local Government', validators=[DataRequired()])

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')