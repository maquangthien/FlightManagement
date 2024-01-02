from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Role(db.Model):
    __tablename__ = 'role'
    role_id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.role_name

class User(db.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey('role.role_id'), nullable=False)
    role = relationship('Role', backref='users')

class Customer(db.Model):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False, unique=True)
    customer_name = Column(String(100), nullable=False)
    cmnd_cccd = Column(String(20), nullable=False, unique=True)
    phone = Column(String(15), nullable=False)

class TicketType(db.Model):
    __tablename__ = 'ticket_type'
    ticket_type_id = Column(Integer, primary_key=True, autoincrement=True)
    type_name = Column(String(50), nullable=False, unique=True)
    class_name = Column(String(20), nullable=False)

class Seat(db.Model):
    __tablename__ = 'seat'
    seat_id = Column(Integer, primary_key=True, autoincrement=True)
    seat_number = Column(String(10), nullable=False, unique=True)
    class_name = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)

class FlightRoute(db.Model):
    __tablename__ = 'flight_route'
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    source_airport_id = Column(Integer, ForeignKey('airport.airport_id'), nullable=False)
    destination_airport_id = Column(Integer, ForeignKey('airport.airport_id'), nullable=False)
    distance = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)

class Flight(db.Model):
    __tablename__ = 'flight'
    flight_id = Column(Integer, primary_key=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey('flight_route.route_id'), nullable=False)
    flight_number = Column(String(20), nullable=False, unique=True)
    aircraft_type = Column(String(50), nullable=False)
    total_seats_h1 = Column(Integer, nullable=False)
    total_seats_h2 = Column(Integer, nullable=False)
    departure_date_time = Column(DateTime, nullable=False)
    arrival_date_time = Column(DateTime, nullable=False)

class Airport(db.Model):
    __tablename__ = 'airport'
    airport_id = Column(Integer, primary_key=True, autoincrement=True)
    airport_name = Column(String(100), nullable=False, unique=True)
    location = Column(String(100), nullable=False)

class FlightSchedule(db.Model):
    __tablename__ = 'flight_schedule'
    schedule_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.flight_id'), nullable=False)
    stopover_airport_id = Column(Integer, ForeignKey('airport.airport_id'))
    stopover_duration = Column(Integer, nullable=False)
    note = Column(String(255))

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(Integer, ForeignKey('flight.flight_id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    ticket_type_id = Column(Integer, ForeignKey('ticket_type.ticket_type_id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seat.seat_id'), nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)

class History(db.Model):
    __tablename__ = 'history'
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    action = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)

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
