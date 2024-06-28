from ehub import db, login_manager, app
from flask_login import UserMixin
from flask import session
from flask_login import current_user
from flask_principal import identity_loaded, UserNeed, RoleNeed

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'role'):
        role = Role.query.filter_by(id = current_user.role_id).first()
        identity.provides.add(RoleNeed(role.name))

stud_course = db.Table('stud_course',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
)                   
          

class Role(db.Model):
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(15), unique=True)
        users = db.relationship('User', backref='role', lazy=True)
    

  

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=35), nullable = False, unique = True)
    email=db.Column(db.String(length=120), nullable = False, unique = True)
    password = db.Column(db.String(length=60), nullable = False)
    image_file = db.Column(db.String(length=20), nullable=False, default='default.jpg')
    biography = db.Column(db.Text, nullable = False)
    expertise = db.Column(db.String(length=25),nullable = False)
    course_type = db.Column(db.String(length=15),nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    courses = db.relationship('Course', backref='instructor', lazy=True)
    

    
    def __repr__(self) -> str:
        return f'Insructor {self.name}, {self.email} {self.course_type} {self.category_id}'
    
class User(db.Model, UserMixin):  
    id = db.Column(db.Integer, primary_key = True)
    email=db.Column(db.String(length=120), nullable = False, unique = True)
    password = db.Column(db.String(length=60), nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=35), nullable = False, unique = True)
    instructors = db.relationship('Instructor', backref='category', lazy=True)
    courses = db.relationship('Course', backref='category', lazy=True)
    
    def __repr__(self) -> str:
        return f'Category {self.id}, {self.name}'
    
        
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=25), nullable = False, unique = True)
    description= db.Column(db.String(length=500), nullable = False)
    image_file = db.Column(db.String(length=20), nullable=False, default='default.jpg')
    course_type = db.Column(db.String(length=15),nullable = False)
    price = db.Column(db.Integer)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    reviews = db.relationship('Review', backref='course', lazy=True)
    
    
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=25), nullable = False, unique = True)
    email=db.Column(db.String(length=120), nullable = False, unique = True)
    password = db.Column(db.String(length=60), nullable = False)
    courses = db.relationship('Course', secondary=stud_course, backref='students_enrolled', lazy=True)
    reviews = db.relationship('Review', backref='student', lazy=True)
    
   
class Review(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, unique = True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

