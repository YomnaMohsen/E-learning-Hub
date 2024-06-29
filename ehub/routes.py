from ehub import app, db, bcrypt
import os
from PIL import Image
import secrets
from ehub.models import *
from flask import render_template, flash, redirect, url_for, session, current_app
from ehub.forms import RegistrationForm, LoginForm, RegistrationForm_Teacher, Add_newcourse_Form
from flask_login import login_user, current_user, logout_user, login_required
from flask_principal import Permission, RoleNeed, identity_changed, Identity, AnonymousIdentity


instructor_Permission= Permission(RoleNeed('Instructor'))
student_Permission= Permission(RoleNeed('Student'))
@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/register-teacher",  methods=['GET', 'POST'])
def register_inst():
   # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
    form = RegistrationForm_Teacher()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        category_obj = Category.query.filter_by(name =form.expertise.data).first()
        if form.type_online.data and form.type_videos.data:
           c_type = "Both"
        elif form.type_online.data:
            c_type = "Online"
        else:
            c_type = "Video"    
        if form.picture.data:
          pic_file = save_picture(form.picture.data)
        else:
            pic_file = "default.png"   
        instructor = Instructor(name=form.username.data, email=form.email.data,biography=form.biography.data,
                        expertise = form.expertise.data, image_file=pic_file,  course_type = c_type,          
                        category_id = category_obj.id, password=hashed_password)
        role = Role.query.filter_by(name ="Instructor").first()
        db.session.add(instructor)
        db.session.commit()
        user = User(email=instructor.email, password=instructor.password, user_id=instructor.id, role_id=role.id)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register_teacher.html', title = "Register as Teacher", form = form)


@app.route("/register",  methods=['GET', 'POST'])
def register_page():
   # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
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
   # if current_user.is_authenticated:
    #    return redirect(url_for('home'))
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


def get_instructordata(user_id):
    user = User.query.filter_by(id =user_id).first()
    teacher = Instructor.query.filter_by(id =user.user_id).first()
    image_file = url_for('static', filename='profile_pics/' + teacher.image_file)
    return teacher, image_file

@app.route("/dash/teacher", methods=['GET', 'POST'])
@login_required
@instructor_Permission.require()
def account_teacher():
    user_id = current_user.id
    teacher, image_file = get_instructordata(user_id)
    return render_template("dashboard_teacher.html", image_file = image_file, name = teacher.name, 
                           expert = teacher.expertise, c_type=teacher.course_type, title="account")
    
@app.route("/dash/teacher/newcourse", methods=['GET', 'POST'])
@login_required
@instructor_Permission.require()
def account_course():
    user_id = current_user.id
    teacher, image_teacher = get_instructordata(user_id)  
    form = Add_newcourse_Form()
    if form.validate_on_submit():
        if form.picture.data:
          pic_file = save_picture(form.picture.data)
        else:
            pic_file = "default.png"   
        course = Course(name=form.name.data, description=form.description.data,
                            image_file=pic_file,  course_type= form.Course_type.data, 
                            price = form.price.data,  instructor_id = teacher.id,category_id =teacher.category_id)
        db.session.add(course)
        db.session.commit()
        flash("Course successfully added", category="success")
        return redirect(url_for('account_teacher'))
    return render_template("new_course.html", image_file = image_teacher, name = teacher.name, 
                           expert = teacher.expertise, c_type=teacher.course_type, form= form,
                           title="New_Course")
 
    
    
@app.route("/dash/student")
@login_required
@student_Permission.require(http_exception=403)
def account_student():
    user_id = current_user.id
    U = User.query.filter_by(id=user_id).first()
    Std = Student.query.filter_by(id=U.user_id).first()
    return render_template("dashboard_student.html", name= Std.name, title="account")    

@app.route("/dash/student/Book")
@login_required
@student_Permission.require(http_exception=403)
def student_Booking():
    return render_template("book_course.html")

@app.route("/logout")
def logout():
    logout_user()
     # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('home'))
    


