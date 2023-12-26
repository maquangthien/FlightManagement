from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True, unique=True)
    identity = Column(String(20), nullable=True)
    _password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.role_id), nullable=False)
    role = relationship(Role)

    def __str__(self):
        return self.name

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, plaintext_password):
        self._password = generate_password_hash(plaintext_password)

    def check_password(self, plaintext_password):
        return check_password_hash(self._password, plaintext_password)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
        # admin_role = Role(role_name='admin')
        # staff_role = Role(role_name='staff')
        # customer_role = Role(role_name='customer')
        #
        # db.session.add_all([admin_role, staff_role, customer_role])
        # db.session.commit()
