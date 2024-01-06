import math

from flask import render_template, request, redirect, url_for
from app import app, login
from flask_login import login_user


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



if __name__ == '__main__':
    from app.admin import *
    app.run(debug=False)
