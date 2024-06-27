from ehub import app, db, bcrypt
from ehub.models import *
from flask import render_template, flash, redirect, url_for, session, current_app
from ehub.forms import RegistrationForm, LoginForm, RegistrationForm_Teacher
from flask_login import login_user, current_user, logout_user, login_required
from flask_principal import Permission, RoleNeed, identity_changed, Identity


instructor_Permission= Permission(RoleNeed('Instructor'))
student_Permission= Permission(RoleNeed('Student'))
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route("/register-teacher",  methods=['GET', 'POST'])
def register_inst():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm_Teacher()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        category_obj = Category.query.filter_by(name =form.expertise.data).first()
        c_type = "Online" if form.type_online.data else "Video"
        instructor = Instructor(name=form.username.data, email=form.email.data,biography=form.biography.data,
                        expertise = form.expertise.data,  course_type = c_type,          
                        category_id = category_obj.id, password=hashed_password)
        role = Role.query.filter_by(name ="Instructor").first()
        db.session.add(instructor)
        db.session.commit()
        user = User(email=instructor.email, password=instructor.password, user_id=instructor.id, role_id=role.id)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_teacher.html', title = "Register as Teacher", form = form)


@app.route("/register",  methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        role = Role.query.filter_by(name ="Student").first()
        student = Student(name=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(student)
        db.session.commit()
        user = User(email=student.email, password=student.password, user_id=student.id, role_id=role.id)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register on Site", form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            role = Role.query.filter_by(id = user.role_id).first()
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.id))
            flash('Login successful!', category='success')
            if role.name == 'Instructor':
                return redirect(url_for('account_teacher'))
            elif role.name == 'Student':
                return redirect(url_for('account_student'))
        else:
            flash('Login unsuccessful, Please check mail and password!', category='danger')
    return render_template('login.html', title = "Login to Site", form = form)


@app.route("/dash/teacher", methods=['GET', 'POST'])
@login_required
@instructor_Permission.require()
def account_teacher():
    user_id = current_user.id
    user = User.query.filter_by(id =user_id).first() 
    print(current_user.password,user.email)
    
    if not user:
        print("None")
        flash('Permission denied', category='danger')
        return render_template("home.html") 
    return render_template("account_teacher.html", title="account")
    
    
@app.route("/dash/student")
@login_required
@student_Permission.require(http_exception=403)
def account_student():
        return render_template("account_std.html", title="account")    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    


