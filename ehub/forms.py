from flask_wtf import FlaskForm
import re
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ehub.models import Student, Category

# Custom validator function
def validate_password_complexity(form, field):
    password = field.data
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    # Compile the pattern
    regex = re.compile(pattern)

    # Match the password against the pattern
    if not regex.match(password):
        raise ValidationError('Email must contain at least one alphabet character, one number, one special character and minimum length 8')
def validate_username(form, field):
        student = Student.query.filter_by(name=field.data).first()
        if student:
            raise ValidationError('That username is already in use. Please choose a different one.')
       

def validate_email(form, email):
    student = Student.query.filter_by(email=email.data).first()
    if student:
        raise ValidationError('That email is already in use. Please choose a different one.')

####################################################################################

def fill_list():
    list_names = []
    list_expertise = Category.query.all()
    list_names.append("Expertise")
    for exp in list_expertise:
        list_names.append(exp.name)
    return list_names    
    

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20), DataRequired(), validate_username])
    email = StringField('Email',
                        validators=[Email(), DataRequired(), validate_email])
    password = PasswordField('Password', validators=[DataRequired(), validate_password_complexity])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Create Account')
    
    
class RegistrationForm_Teacher(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20), validate_username])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), validate_email])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(min=10)])
    expertise = SelectField('Expertise', choices= fill_list, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_password_complexity])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')