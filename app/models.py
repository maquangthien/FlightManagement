from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Permission(db.Model):
    __tablename__ = 'permission'
    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(255), nullable=False)
    permission_details = db.relationship('PermissionDetails', backref='permission', lazy=True)


class Position(db.Model):
    __tablename__ = 'position'
    position_id = db.Column(db.Integer, primary_key=True)
    position_name = db.Column(db.String(255), nullable=False)
    permission_details = db.relationship('PermissionDetails', backref='position', lazy=True)


class PermissionDetails(db.Model):
    __tablename__ = 'permissionDetails'
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.permission_id'), nullable=False)
    position = db.relationship('Position', backref='permission_details')
    permission = db.relationship('Permission', backref='permission_details')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    dob = db.Column(db.DateTime, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    identity = db.Column(db.String(20), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'), nullable=True)
    position = db.relationship('Position', backref='users')
    account = db.relationship('Account', backref='user', lazy=True)
    permission_details = db.relationship('PermissionDetails', backref='user')


class Account(db.Model):
    __tablename__ = 'account'
    account_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


class TicketType(db.Model):
    __tablename__ = 'ticketType'
    ticket_type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(255), nullable=False)
    fare = db.Column(db.Float, nullable=False)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref='tickets')
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.flight_id'), nullable=False)
    flight = db.relationship('Flight', backref='tickets')
    ticket_type_id = db.Column(db.Integer, db.ForeignKey('ticketType.ticket_type_id'), nullable=False)
    ticket_type = db.relationship('TicketType', backref='tickets')
    status = db.Column(db.String(50), nullable=True)


class Invoice(db.Model):
    invoice_id = db.Column(db.Integer, primary_key=True)
    invoice_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Flight(db.Model):
    __tablename__ = 'flight'
    flight_id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=False)
    plan = db.relationship('Plan', backref='flights')
    flight_number = db.Column(db.String(50), nullable=False)
    departure_date_time = db.Column(db.DateTime, nullable=False)
    arrival_date_time = db.Column(db.DateTime, nullable=False)
    flight_status = db.Column(db.String(50), nullable=True)
    flight_route_id = db.Column(db.Integer, db.ForeignKey('flight_route.flight_route_id'), nullable=False)
    flight_route = db.relationship('FlightRoute', backref='flights')


class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    aircraft_name = db.Column(db.String(255), nullable=False)
    aircraft_type = db.Column(db.String(50), nullable=False)
    aircraft_cabin = db.Column(db.String(50), nullable=False)
    total_seats_h1 = db.Column(db.Integer, nullable=False)
    total_seats_h2 = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=True)

    airline_id = db.Column(db.Integer, db.ForeignKey('airline.airline_id'), nullable=False)
    airline = db.relationship('Airline', backref='plans')

    flights = db.relationship('Flight', backref='plan', lazy=True)


class Seat(db.Model):
    seat_id = db.Column(db.Integer, primary_key=True)
    seat_number = db.Column(db.String(10), nullable=False)
    class_seat = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), nullable=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=False)
    plan = db.relationship('Plan', backref='seats')


class Airport(db.Model):
    airport_code = db.Column(db.String(3), primary_key=True)
    airport_name = db.Column(db.String(255), nullable=False)
    airport_location = db.Column(db.String(255), nullable=False)

    flightroutedetails = db.relationship('FlightRouteDetails', backref='airport')


class FlightRoute(db.Model):
    flight_route_id = db.Column(db.Integer, primary_key=True)
    departure_airport = db.Column(db.String(50), nullable=False)
    destination_airport = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=True)
    distance = db.Column(db.Float, nullable=True)

    flightroutedetails = db.relationship('FlightRouteDetails', backref='flight_route')


class FlightRouteDetails(db.Model):
    flightroutedetails_id = db.Column(db.Integer, primary_key=True)
    airport_code = db.Column(db.String(3), db.ForeignKey('airport.airport_code'), nullable=False)
    flight_route_id = db.Column(db.Integer, db.ForeignKey('flight_route.flight_route_id'), nullable=False)
    airport_name = db.Column(db.String(255), nullable=False)
    intermediate_airport = db.Column(db.Boolean, nullable=False)
    duration = db.Column(db.String(50), nullable=True)
    note = db.Column(db.String(255), nullable=True)

    airport = db.relationship('Airport', backref='flightroutedetails')
    flight_route = db.relationship('FlightRoute', backref='flightroutedetails')


class Airline(db.Model):
    airline_id = db.Column(db.Integer, primary_key=True)
    airline_name = db.Column(db.String(255), nullable=False)

    plans = db.relationship('Plan', backref='airline', lazy=True)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()
