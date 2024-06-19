from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'e-learn.db')
app.config['SECRET_KEY'] = '13547cd85dc99262d5399635'
db = SQLAlchemy(app)

from ehub import routes