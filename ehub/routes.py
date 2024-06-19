from ehub import app
from flask import render_template
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


