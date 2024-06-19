from ehub import app
from flask import render_template, flash, redirect, url_for
from ehub.forms import RegistrationForm, LoginForm
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
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = "Register as Teacher", form = form)


@app.route("/register",  methods=['GET', 'POST'])
def register_inst():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created successfully for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title = "Register on Site", form = form)

@app.route("/login")
def login_page():
    form = LoginForm()
    return render_template('login.html', title = "Login to Site", form = form)
    


