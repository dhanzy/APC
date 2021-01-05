import pycountry
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextField, SelectField, SubmitField, PasswordField, IntegerField, StringField, FileField, BooleanField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
import phonenumbers

from APC.model import User


test = [('Ado','Ado'),('Efon','Efon'),('Omuo','Omuo'), ('Aramoko','Aramoko'), ('Erijiyan','Erijiyan'),\
        ('Ikogosi','Ikogosi'), ('Okemesi','Okemesi'),('Ido Ajinare', 'Ido Ajinare'),('Ilawe', 'Ilawe'),\
        ('Igbara Odo','Igbara Odo'), ('Ogotun', 'Ogotun'), ('Emure','Emure'),('Gboyin', 'Gboyin'),('Ido-Osi','Ido-Osi'),\
        ('Ijero','Ijero'),('Ipoti','Ipoti'),('Odo Owa','Odo Owa'),('Iloro','Iloro'),('Ikoro','Ikoro'),('Ekamarun','Ekamarun'),\
        ('Ekameta','Ekameta'),('Ikere','Ikere'),('Ikole','Ikole'),('Ilejemeje','Ilejemeje'),('Irepodun/Ifelodun','Irepodun/Ifelodun'),\
        ('Ise/Orun','Ise/Orun'),('Moba','Moba'),('Oye','Oye')
    ]
LocalGoverment = [('Ado-Ekiti', 'Ado-Ekiti'), ('Ikere','Ikere'),('Oye','Oye'), ('Aiyekire (Gbonyin)','Aiyekire (Gbonyin)'), \
        ('Efon','Efon'), ('Ekiti East','Ekiti East'),('Ekiti South-West','Ekiti South-West'),('Ekiti West','Ekiti West'), \
        ('Emure','Emure'),('Ido-Osi','Ido-Osi'),('Ijero','Ijero'),('Ikole','Ikole'),('Ilejemeje','Ilejemeje'), \
        ('Irepodun/Ifelodun','Irepodun/Ifelodun'),('Ise/Orun','Ise/Orun'),('Moba','Moba')
    ]   

class LoginForm(FlaskForm):
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=11, max=16)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
            if phone.data == '':
                raise ValidationError('Phone Number required')
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')



class RegisterForm(FlaskForm):
    firstname =StringField('First Name', validators=[DataRequired(), Length(max=32)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=32)])
    phone = StringField('Phone',  validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male','Male'), ('female','Female')])
    profile_image = FileField('Update Image', validators=[FileAllowed(['jpg','png'])])
    state = SelectField('State', choices=[('Ekiti','Ekiti')])
    ward = SelectField('Ward', choices=[str(i) for i in range(1,14)])
    city = StringField('Town', validators=[DataRequired(), Length(max=30)])
    lga = SelectField('Local Government', choices=LocalGoverment)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_phone(self, phone):
    
        try:
            p = phonenumbers.parse(phone.data)
            print('Number ', p)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
            if phone.data == '':
                raise ValidationError('Phone Number required!')
            user = User.query.filter_by(phone=phone.data).first()
            print('Getting User: ', user)
            if user:
                print('User already registered')
                raise UserWarning
            print('Validated correctly')
            
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            print('Invalid Phone number: ', phone.data)
            raise ValidationError('Invalid phone number!')

        except UserWarning:
            raise ValidationError('User Already Registered!')



class UploadImageForm(FlaskForm):
    profile_image = FileField('Update Image', validators=[FileAllowed(['jpg','png'])])
    submit_btn = SubmitField("Update Profile")



class ChangePassword(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Update Password')