from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flaskr import app

db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    firstname = db.Column(db.String(20), nullable=False)
    secondname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="customer")
    bookings = db.relationship('Booking', back_populates='user')

    def __init__(self, email, password, firstname, secondname, role='customer'):
        self.email = email
        self.password = password
        self.firstname = firstname
        self.secondname = secondname
        self.role = role

    def __repr__(self):
        return f'<User {self.email!r}>'


class AirLine(db.Model):
    __tablename__ = 'airline'
    id = db.Column(db.Integer, autoincrement=True,
                   unique=True, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    flights = db.relationship("Flight", back_populates='airline')
    # admin = db.relationship('user', back_populates='airline')

    def __init__(self, admin_id, name):
        self.admin_id = admin_id
        self.name = name

    def __repr__(self):
        return f'<Airline {self.name!r}>'


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<City {self.name!r}>'


class Flight(db.Model):
    __tablename__ = 'flight'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    airline_id = db.Column(db.Integer, db.ForeignKey(
        "airline.id"), nullable=False)
    origin_city_id = db.Column(db.Integer, db.ForeignKey(
        "city.id"), nullable=False, index=True)
    destination_city_id = db.Column(
        db.Integer, db.ForeignKey("city.id"), nullable=False, index=True)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seats = db.relationship('Seat', back_populates='flight')
    airline = db.relationship('AirLine', back_populates='flights')
    # origin_city = db.relationship('city', back_populates='flight')
    # destination_city = db.relationship('city', back_populates='flight')

    def __init__(self, airline_id, origin_city_id, destination_city_id, total_seats, available_seats, departure_time, duration, price, ):
        self.airline_id = airline_id
        self.origin_city_id = origin_city_id
        self.destination_city_id = destination_city_id
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.departure_time = departure_time
        self.duration = duration
        self.price = price

    def __repr__(self):
        return f'<Flight {self.airline_id, self.origin_city_id, self.destination_city_id!r}>'


class Seat(db.Model):
    __tablename__ = 'seat'
    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, unique=True)
    flight_id = db.Column(db.Integer, db.ForeignKey(
        'flight.id'), nullable=False)
    seat_number = db.Column(db.String(20), nullable=False)
    is_occupied = db.Column(db.Boolean, default=False)
    flight = db.relationship('Flight', back_populates='seats')

    def __init__(self, flight_id, seat_number, is_occupied, flight):
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.is_occupied = is_occupied
        self.flight = flight

    def __repr__(self):
        return f'<Seat {self.seat_number, self.flight!r}>'


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True,
                   unique=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey(
        'flight.id'), nullable=False)
    seat_id = db.Column(db.Integer, db.ForeignKey('seat.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.now())
    user = db.relationship('User', back_populates='bookings')
    # flight = db.relationship('Flight', back_populates='booking')
    # seat = db.relationship('Seat', back_populates='booking')

    def __init__(self, user_id, flight_id, seat_id):
        self.user_id = user_id
        self.flight_id = flight_id
        self.seat_id = seat_id
        self.booked_at = datetime.now()

    def __repr__(self):
        return f'<Booking {self.flight, self.seat, self.user!r}>'
