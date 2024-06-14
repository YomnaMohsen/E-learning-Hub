from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'e-learn.db')
db = SQLAlchemy(app)

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(length=35), nullable = False, unique = True)
    email=db.Column(db.String(length=120), nullable = False, unique = True)
    password = db.Column(db.String(length=60), nullable = False)
    #image_file = db.Column(db.String(length=20), nullable=False, default='default.jpg')
    biography = db.Column(db.Text, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    courses = db.relationship('Course', backref='instructor', lazy=True)
    
    def __repr__(self) -> str:
        return f'Insructor {self.user_name}, {self.email} {self.biography}'
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=35), nullable = False, unique = True)
    instructors = db.relationship('Instructor', backref='category', lazy=True)
    courses = db.relationship('Course', backref='category', lazy=True)
        
    
class Course(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=25), nullable = False, unique = True)
    description= db.Column(db.String(length=500), nullable = False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    
class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(length=25), nullable = False, unique = True)
    email=db.Column(db.String(length=120), nullable = False, unique = True)
    password = db.Column(db.String(length=60), nullable = False)
    
    



@app.route('/')
@app.route('/home')
def hello():
    posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')

if __name__ == '__main__':
    app.run(debug=True)

