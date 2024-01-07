from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import cloudinary

import cloudinary.api

app = Flask(__name__)

app.secret_key = '^%*&^^HJGHJGHJFD%^&%&*^*(^^^&^(*^^$%^GHJFGHJH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/flight' % quote('17Hoang08@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)


CLOUDINARY_URL = 'cloudinary://137131721752293:2piWuAlUnTFlpWCaDI8BKiObYoo@dtcjtwznh'
cloudinary.config(
    cloud_name="dtcjtwznh",
    api_key="137131721752293",
    api_secret="2piWuAlUnTFlpWCaDI8BKiObYoo",
    secure=True
)
