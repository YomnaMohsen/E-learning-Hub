from ehub import app, db, bcrypt
import os
from PIL import Image
import secrets
from ehub.models import *
from flask import render_template, flash, redirect, url_for, session, current_app, request
from ehub.forms import *
from flask_login import login_user, current_user, logout_user, login_required
from flask_principal import Permission, RoleNeed, identity_changed, Identity, AnonymousIdentity
from werkzeug.utils import secure_filename
import uuid as uuid


instructor_Permission= Permission(RoleNeed('Instructor'))
student_Permission= Permission(RoleNeed('Student'))
@app.route('/')
@app.route('/home', strict_slashes=False)
def home():
    return render_template("homepage.html")

##############################################################################
# Helper fn
def save_picture(f_name):
    file_name = secure_filename(f_name)
    pic_name = str(uuid.uuid1()) + '_' + file_name
    saver = request.files['picture']
    basedir = os.path.abspath(os.path.dirname(__file__))
    saver.save(os.path.join(basedir, app.config['UPLOAD_FOLDER'], pic_name))
    return pic_name
################################################################################
def get_instructordata(user_id):
    user = User.query.filter_by(id =user_id).first()
    teacher = Instructor.query.filter_by(id =user.user_id).first()
    image_file = teacher.image_file
    return teacher, image_file
##################################################################################
def get_std_data(user_id):
    user = User.query.filter_by(id =user_id).first()
    student = Student.query.filter_by(id =user.user_id).first()
    return student
################################################################################


# Registeration
@app.route("/register-teacher",  methods=['GET', 'POST'], strict_slashes=False)
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
        instructor = Instructor(name=form.username.data, email=form.email.data,biography=form.biography.data,
                        expertise = form.expertise.data, image_file=request.files['picture'],  course_type = c_type,          
                        category_id = category_obj.id, password=hashed_password)
        instructor.image_file=save_picture(instructor.image_file.filename)
        db.session.add(instructor)
        db.session.commit()
        role = Role.query.filter_by(name ="Instructor").first()
        user = User(email=instructor.email, password=instructor.password, user_id=instructor.id, role_id=role.id)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    if form.errors != {}: 
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register_teacher.html', title = "Register as Teacher", form = form)


@app.route("/register",  methods=['GET', 'POST'], strict_slashes=False)
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



########################################################################33
#login
@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
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

#################################################################################
#Dashboard
@app.route("/dash/teacher/profile", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@instructor_Permission.require()
def account_teacher():
    user_id = current_user.id
    teacher, image_file = get_instructordata(user_id)
    return render_template("inst_profile.html", image_file = image_file, name = teacher.name, 
                           expert = teacher.expertise, c_type=teacher.course_type, title="account")


@app.route("/dash/teacher/newcourse", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@instructor_Permission.require()
def account_course():
    user_id = current_user.id
    teacher, image_teacher = get_instructordata(user_id)  
    form = Add_newcourse_Form()
    if form.validate_on_submit():
        course = Course(name=form.name.data, description=form.description.data,
                            image_file=request.files['picture'],  course_type= form.Course_type.data, 
                            price = form.price.data,  instructor_id = teacher.id,
                            category_id =teacher.category_id)
        course.image_file=save_picture(course.image_file.filename)
        db.session.add(course)
        db.session.commit()
        flash("Course successfully added", category="success")
        return redirect(url_for('account_teacher'))
    return render_template("new_course.html", image_file = image_teacher, name = teacher.name, 
                           expert = teacher.expertise, c_type=teacher.course_type, form= form,
                           title="New_Course")
    
    
    
@app.route("/dash/teacher/editcourse", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@instructor_Permission.require()
def edit_course():
    user_id = current_user.id
    teacher, image_teacher = get_instructordata(user_id)
    C = teacher.courses
    form = Edit_course_Form()
    if form.validate_on_submit():
        for C_obj in C:
            if form.name.data == C_obj.name:
                break
        if form.description.data:
            C_obj.description = form.description.data
        
        if form.price.data:
            C_obj.price = form.price.data
        
        if form.Course_type.data:
            C_obj.course_type = form.Course_type.data          
        
        if form.picture.data:
            C_obj.image_file = save_picture(form.picture.data.filename)
        db.session.commit()
        flash("Course successfully edited", category="success")
        return redirect(url_for('account_teacher'))
    return render_template("inst_edit_course.html", image_file = image_teacher, name = teacher.name, 
                           expert = teacher.expertise, c_type=teacher.course_type, form= form,
                           title="Edit_Course")    
 
@app.route("/dash/teacher/viewcourses", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@instructor_Permission.require()
def view_courses(): 
    user_id = current_user.id
    teacher, image_teacher = get_instructordata(user_id)
    return render_template("inst_all_courses.html", image_file = image_teacher, name = teacher.name, 
                          expert = teacher.expertise,  c_list=teacher.courses, c_type=teacher.course_type, title="View_Courses")
    
###############################################################################################################    
@app.route("/dash/student/profile", strict_slashes=False)
@login_required
@student_Permission.require(http_exception=403)
def account_student():
    user_id = current_user.id
    student = get_std_data(user_id)
    return render_template("dashboard_student.html", name= student.name, title="account")  
######################################################################################

##############################################################################
#Courses mang.
@app.route("/dash/student/Book", methods=['GET', 'POST'], strict_slashes=False)
@app.route("/dash/student/Book/<int:id>", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@student_Permission.require(http_exception=403)
def student_Booking(id = 0):
    user_id = current_user.id
    student = get_std_data(user_id)
    if id != 0:
        C = Course.query.filter_by(id = id).first()
        if C in student.courses:
            flash ("already booked")
        else:    
            student.courses.append(C)
            db.session.commit()
        return redirect (url_for("account_student", name= student.name, title="account"))
    form = Book_newcourse_Form()
    if form.validate_on_submit():
    
       if form.instructor.data != "Instructor":
           inst = Instructor.query.filter_by(name=form.instructor.data).first()
           return render_template('book_inst_course.html', c_list = inst.courses) 
       elif form.expertise.data != "Expertise":
           cat = Category.query.filter_by(name= form.expertise.data).first() 
           return render_template('book_inst_course.html', c_list = cat.courses)   
    return render_template("book_course.html",form=form,name= student.name, 
                           title="Booking")
    
    
@app.route("/dash/student/Booked_courses", methods=['GET', 'POST'], strict_slashes=False)
@login_required
@student_Permission.require(http_exception=403)
def Booked_course():
    user_id = current_user.id
    student = get_std_data(user_id)
    stud =  Student.query.filter_by(id=student.id).first()
    return render_template("view_booked_courses.html", list_c = stud.courses)
     
##########################################################################
@app.route("/logout", strict_slashes=False)
def logout():
    logout_user()
     # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())
    return redirect(url_for('home'))
    


