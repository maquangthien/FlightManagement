import math

from flask import render_template, request, redirect, url_for
import dao
from app import app, login
from flask_login import login_user


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin/login', methods=['POST'])
def login_admin_process():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == '__main__':
    from app import admin
    app.run(debug=False)
