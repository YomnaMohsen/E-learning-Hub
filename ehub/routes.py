from ehub import app, db, bcrypt
from ehub.models import Student, Instructor, Category
from flask import render_template, flash, redirect, url_for
from ehub.forms import RegistrationForm, LoginForm, RegistrationForm_Teacher
from flask_login import login_user, current_user, logout_user
@app.route('/')
@app.route('/home')
def home():
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

@app.route("/register-teacher",  methods=['GET', 'POST'])
def register_inst():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm_Teacher()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        category_obj = Category.query.filter_by(name =form.expertise.data).first()
        instructor = Instructor(user_name=form.username.data, email=form.email.data,biography=form.biography.data, category_id= category_obj.id,
                                password=hashed_password)
        db.session.add(instructor)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login_page'))
    return render_template('register_teacher.html', title = "Register as Teacher", form = form)


@app.route("/register",  methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title = "Register on Site", form = form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            return redirect(url_for('home'))
    return render_template('login.html', title = "Login to Site", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    


