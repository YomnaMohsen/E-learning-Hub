from flask_wtf import FlaskForm
import re
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

# Custom validator function
def validate_email_complexity(form, field):
    password = field.data
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    # Compile the pattern
    regex = re.compile(pattern)

    # Match the password against the pattern
    if not regex.match(password):
        raise ValidationError('Email must contain at least one alphabet character, one number, one special character and minimum length 8')


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20), DataRequired()])
    email = StringField('Email',
                        validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), validate_email_complexity])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField('Create Account')
    
    
class RegistrationForm_Teacher(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    biography = TextAreaField('Biography', validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_email_complexity])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')