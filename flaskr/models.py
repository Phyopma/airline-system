from flaskr.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Session, relationship, sessionmaker
from datetime import datetime


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    firstname = Column(String(20), nullable=False)
    secondname = Column(String(20), nullable=False)
    role = Column(String(20), nullable=False, default="customer")
    bookings = relationship('Booking', back_populates='user')

    def __init__(self, email, password, first, second, role):
        self.email = email
        self.password = password
        self.firstname = first
        self.secondname = second
        self.role = role

    def __repr__(self):
        return f'<User {self.email!r}>'


class AirLine(Base):
    __tablename__ = 'airline'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    admin_id = Column(Integer, ForeignKey("user_id"), nullable=False)
    name = Column(String(50), nullable=False)
    flights = relationship("Flight", back_populates='airline')
    # admin = relationship('user', back_populates='airline')

    def __init__(self, admin_id, name):
        self.admin_id = admin_id
        self.name = name

    def __repr__(self):
        return f'<Airline {self.name!r}>'


class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, unique=True, primary_key=True)
    name = Column(String(50), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<City {self.name!r}>'


class Flight(Base):
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    airline_id = Column(Integer, ForeignKey("airline.id"), nullable=False)
    origin_city_id = Column(Integer, ForeignKey(
        "city.id"), nullable=False, index=True)
    destination_city_id = Column(
        Integer, ForeignKey("city.id"), nullable=False, index=True)
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    duration = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    seats = relationship('Seat', back_populates='flight')
    airline = relationship('AirLine', back_populates='flights')
    # origin_city = relationship('city', back_populates='flight')
    # destination_city = relationship('city', back_populates='flight')

    def __init__(self, airline_id, origin_city_id, destination_city_id, total_seats, available_seats, departure_time, duration, price):
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


class Seat(Base):
    __tablename__ = 'seat'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    seat_number = Column(String(20), nullable=False)
    is_occupied = Column(Boolean, default=False)
    flight = relationship('Flight', back_populates='seats')

    def __init__(self, flight_id, seat_number, is_occupied, flight):
        self.flight_id = flight_id
        self.seat_number = seat_number
        self.is_occupied = is_occupied
        self.flight = flight

    def __repr__(self):
        return f'<Seat {self.seat_number, self.flight!r}>'


class Booking(Base):
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    flight_id = Column(Integer, ForeignKey('flight.id'), nullable=False)
    seat_id = Column(Integer, ForeignKey('seat.id'), nullable=False)
    booked_at = Column(DateTime, default=datetime.now())
    user = relationship('User', back_populates='bookings')
    # flight = relationship('Flight', back_populates='booking')
    # seat = relationship('Seat', back_populates='booking')

    def __init__(self, user_id, flight_id, seat_id, booked_at):
        self.user_id = user_id
        self.flight_id = flight_id
        self.seat_id = seat_id
        self.booked_at = booked_at

    def __repr__(self):
        return f'<Booking {self.flight, self.seat, self.user!r}>'
