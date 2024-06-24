from ehub import app, db, bcrypt
from ehub.models import Student, Instructor, Category
from flask import render_template, flash, redirect, url_for, session
from ehub.forms import RegistrationForm, LoginForm, RegistrationForm_Teacher
from flask_login import login_user, current_user, logout_user, login_required
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


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
        c_type = "Online" if form.type_online.data else "Video"
        instructor = Instructor(user_name=form.username.data, email=form.email.data,biography=form.biography.data,
                        expertise = form.expertise.data,  course_type = c_type,          
                        category_id= category_obj.id, password=hashed_password)
        db.session.add(instructor)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login_page1'))
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
        return redirect(url_for('login_page2'))
    return render_template('register.html', title = "Register on Site", form = form)

@app.route("/login/teacher", methods=['GET', 'POST'])
def login_page1():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        instructor = Instructor.query.filter_by(email=form.email.data).first()
        if instructor and bcrypt.check_password_hash(instructor.password, form.password.data):
            login_user(instructor, remember=form.remember.data)
            session.permanent = True
            session['type'] = 'instructor'
            flash('Login successful!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Please check mail and password!', category='danger')
    return render_template('login.html', title = "Login to Site", form = form)



@app.route("/login/student", methods=['GET', 'POST'])
def login_page2():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student, remember=form.remember.data)
            session.permanent = True
            session['type'] = 'student'
            flash('Login successful!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful, Please check mail and password!', category='danger')
    return render_template('login.html', title = "Login to Site", form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    

@app.route("/account/teacher")
@login_required
def account_teacher():
        return render_template("account.html", title="account")
