from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from sqlalchemy import ForeignKeyConstraint
class Account(db.Model):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='account')

# Trong class User
class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    dob = db.Column(DateTime, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    citizen_identity_card= db.Column(db.String(20), nullable=True)
    account = relationship('Account', back_populates='user', uselist=False)
    permissions = relationship('Permission', back_populates='user')
    tickets = relationship('Ticket', back_populates='user')

class Permission(db.Model):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    permission_details = relationship('PermissionDetails', back_populates='permission')
    user = relationship('User', back_populates='permissions')

class PermissionDetails(db.Model):
    __tablename__ = 'permission_details'
    id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey('permission.id'))
    position_id = Column(Integer, ForeignKey('position.id'))
    permission = relationship('Permission', back_populates='permission_details')
    position = relationship('Position', back_populates='permission_details')

class Position(db.Model):
    __tablename__ = 'position'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    permission_details = relationship('PermissionDetails', back_populates='position')

class TicketType(db.Model):
    __tablename__ = 'ticket_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    tickets = relationship('Ticket', back_populates='type')

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    type_id = Column(Integer, ForeignKey('ticket_type.id'), nullable=False)
    user = relationship('User', back_populates='tickets')
    flight = relationship('Flight', back_populates='tickets')
    type = relationship('TicketType', back_populates='tickets')

class Flight(db.Model):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True)
    departure_location = Column(String(50), nullable=False)
    destination_location = Column(String(50), nullable=False)
    departure_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    tickets = relationship('Ticket', back_populates='flight')
    route_id = Column(Integer, ForeignKey('routes.id'), nullable=False)
    route = relationship('Routes', back_populates='flights')
    details = relationship('FlightDetails', back_populates='flight')
    airplane_id = Column(Integer, ForeignKey('airplane.id'), nullable=False)
    airplane = relationship('Airplane', back_populates='flights')

class Routes(db.Model):
    __tablename__ = 'routes'
    id = Column(Integer, primary_key=True)
    origin = Column(String(50), nullable=False)
    destination = Column(String(50), nullable=False)
    flights = relationship('Flight', back_populates='route')

class Airline(db.Model):
    __tablename__ = 'airline'
    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True)
    name = Column(String(50), nullable=False, unique=True)
    airplanes = relationship('Airplane', back_populates='airline')

class Airport(db.Model):
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    code = Column(String(3), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    departures = relationship('FlightDetails', foreign_keys='FlightDetails.departure_airport_id', back_populates='departure_airport')
    arrivals = relationship('FlightDetails', foreign_keys='FlightDetails.arrival_airport_id', back_populates='arrival_airport')

class FlightDetails(db.Model):
    __tablename__ = 'flight_details'
    id = Column(Integer, primary_key=True)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    departure_airport_id = Column(Integer, ForeignKey('airport.id'))
    arrival_airport_id = Column(Integer, ForeignKey('airport.id'))

    departure_airport = relationship('Airport', foreign_keys=[departure_airport_id], back_populates='departures')
    arrival_airport = relationship('Airport', foreign_keys=[arrival_airport_id], back_populates='arrivals')

    flight = relationship('Flight', back_populates='details')

class Airplane(db.Model):
    __tablename__ = 'airplane'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    flights = relationship('Flight', back_populates='airplane')
    seats = relationship('Seat', back_populates='airplane')
    airline_id = Column(Integer, ForeignKey('airline.id'), nullable=False)
    airline = relationship('Airline', back_populates='airplanes')

class Seat(db.Model):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    airplane_id = Column(Integer, ForeignKey('airplane.id'), nullable=False)
    airplane = relationship('Airplane', back_populates='seats')

    # Thêm foreign key constraint
    ForeignKeyConstraint([airplane_id], ['airplane.id'])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # # Tạo các chức vụ
        # cv1 = Position(name="Admin")
        # cv2 = Position(name="Employee")
        # cv3 = Position(name="customer")
        #
        # db.session.add_all([cv1, cv2, cv3])
        # db.session.commit()
        #

        ##tạo tài khoản


        # # Tạo giá vé
        # v1 = TicketType(name="Hạng 1")
        # v2 = TicketType(name="Hạng 2")
        # db.session.add_all([v1, v2])
        # db.session.commit()
        #
        # #Tạo hãng máy bay
        # h1= Airline(code="HVN", name = "Hãng hàng không Vietnam Airlines")
        # h2= Airline(code="QH", name = "Hãng hàng không Bamboo Airways")
        # h3= Airline(code="FWL", name = "Florida West International Airways")
        # db.session.add_all([h1, h2, h3])
        # db.session.commit()

        ##Tạo sân bay
        # sb1 = Airport(code="BMV",name="Sân bay Buôn Ma Thuột", location="Đắk Lắk")
        # sb2 = Airport(code="DAD",name="Sân bay quốc tế Đà Nẵng	",location="Đà Nẵng")
        # sb3 = Airport(code="HAN",name="Sân bay quốc tế Nội Bài	", location="Hà Nội	")
        # sb4 = Airport(code="SGN",name="Sân bay quốc tế Tân Sơn Nhất", location="Thành phố Hồ Chí Minh")
        # sb5 = Airport(code="CXR",name="Sân bay quốc tế Cam Ranh", location="Khánh Hòa")
        # sb6 = Airport(code="PQC",name="Sân bay quốc tế Phú Quốc", location="Kiên Giang")
        # sb7 = Airport(code="NGO",name="Sân bay quốc tế Chubu", location="Nagoya")
        # sb8 = Airport(code="ICN",name="Sân bay quốc tế Incheon", location="Hàn Quốc")
        # sb9 = Airport(code="LAX",name="Sân bay quốc tế Los Angeles", location="Los Angeles")
        # sb10 = Airport(code="MVD",name="Sân bay quốc tế Carrasco", location="Montevideo")
        # db.session.add_all([sb1, sb2,sb3, sb4, sb5, sb6, sb7, sb8, sb9, sb10])
        # db.session.commit()
