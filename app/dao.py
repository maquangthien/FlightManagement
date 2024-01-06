from app.models import Role, User
from app import app, db
import hashlib
import json

def auth_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None
