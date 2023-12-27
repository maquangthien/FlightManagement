from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Role(db.Model):
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.role_name


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(50), nullable=True, unique=True)
    identity = Column(String(20), nullable=True)
    _password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('role.role_id'), nullable=False)
    role = relationship(Role)
    tickets = relationship('Ticket', backref='passenger', lazy=True)

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


class Airport(db.Model):
    airport_code = Column(String(3), primary_key=True)
    airport_name = Column(String(50), nullable=False, unique=True)
    airport_location = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.airport_name


class Flight(db.Model):
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    departure_datetime = Column(DateTime, nullable=False)
    flight_duration = Column(Integer, nullable=False)
    available_seats_first_class = Column(Integer, nullable=False)
    available_seats_second_class = Column(Integer, nullable=False)
    tickets = relationship('Ticket', backref='flight', lazy=True)


class IntermediateAirport(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    airport_code = Column(String(3), ForeignKey('airport.airport_code'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flight.flight_id'), nullable=False)
    stop_order = Column(Integer, nullable=False)
    stop_duration = Column(Integer, nullable=False)


class Ticket(db.Model):
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.flight_id'), nullable=False)
    passenger_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    ticket_class = Column(String(20), nullable=False)
    ticket_price = Column(Float, nullable=False)
    booking_time = Column(DateTime, nullable=False)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
        # Thêm dữ liệu mẫu hoặc các thao tác khác ở đây nếu cần.

        # admin_role = Role(role_name='admin')
        # staff_role = Role(role_name='staff')
        # customer_role = Role(role_name='customer')
        #
        # db.session.add_all([admin_role, staff_role, customer_role])

        # f1 = Ariport(airport_code='SGN', airport_name='Sân bay Tân Sân Nhất', airport_location='TP HCM')
        # f2 = Ariport(airport_code='HAN', airport_name='Sân bay quốc tế Nội Bài', airport_location='Hà Nội')
        # db.session.add_all([f1, f2])
        # db.session.commit()
