from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import re
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ehub.models import Student, Category, Instructor, User, Course
from flask_login import current_user

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
        instructor = Instructor.query.filter_by(name=field.data).first()
        if student or instructor:
            raise ValidationError('That username is already in use. Please choose a different one.')
       

def validate_email(form, email):
    student = Student.query.filter_by(email=email.data).first()
    instructor = Instructor.query.filter_by(email=email.data).first()
    if student or instructor:
        raise ValidationError('That email is already in use. Please choose a different one.')

def validate_name(form, name):
    C = Course.query.filter_by(name=name.data).first()
    if C:
        raise ValidationError('Course name already exists')

#############################################################################################


def fill_Inst_list():
    list_names = []
    list_inst = Instructor.query.all()
    list_names.append("Instructor")
    for I in list_inst:
        list_names.append(I.name)
    return list_names

def fill_course_list():
    list_names = []
    list_expertise = Category.query.all()
    list_names.append("Expertise")
    for exp in list_expertise:
        list_names.append(exp.name)
    return list_names
  
######################################################################################3
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
    expertise = SelectField('Expertise', choices= fill_course_list, validators=[DataRequired()])
    picture = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    type_online = BooleanField('Online')
    type_videos = BooleanField('Videos')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8), validate_password_complexity])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')
    
    # check one of the boxes are checked
    def validate(self, extra_validators=None):
        if super().validate(extra_validators):

            # your logic here e.g.
            if not (self.type_online.data or self.type_videos.data):
                self.type_online.errors.append('At least one field must have a value')
                return False
            else:
                return True

        return False
    
class Add_newcourse_Form(FlaskForm):
    name = StringField('Course Name',
                           validators=[DataRequired(), validate_name, Length(min=2, max=20)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    picture = FileField('Upload Course Picture', validators=[FileAllowed(['jpg', 'png'])])
    Course_type = SelectField("Course Type",choices=["Select Course Type", "Online", "Videos"], validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    Add_Course = SubmitField('Add Course')

 
class Book_newcourse_Form(FlaskForm):
    instructor = SelectField("Instructor",choices=fill_Inst_list, validators=[DataRequired()])
    expertise = SelectField('Expertise', choices= fill_course_list, validators=[DataRequired()])
    Search   = SubmitField('Search')
    
class course_inst(FlaskForm):
    type_online = BooleanField('Online')
    type_videos = BooleanField('Videos')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')