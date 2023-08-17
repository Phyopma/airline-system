from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime


from flaskr.models import Flight, db, Seat

from sqlalchemy import select, delete, update, insert


seat_bp = Blueprint('seats', __name__, url_prefix='/seats')


# @seat_bp.get('/<int:flight_id>/')
# def get_all_seats(flight_id):
#     error = None

#     try:
#         seats = db.session.execute(select(Seat).filter(
#             Seat.flight_id == flight_id, Seat.is_occupied == False)).scalars().all()
#     except Exception as e:
#         print(e)
#         abort(500)

#     return render_template('/index.html', seats=seats)


# @seat_bp.get('/<int:airline_id>/')
# def get_flights_by_airline_id(airline_id):
#     error = None

#     try:
#         flights = db.session.execute(
#             select(Flight).filter_by(airline_id=airline_id))
#     except Exception as e:
#         print(e)
#         abort(500)

#     return render_template('/index.html', flights=flights)


# @seat_bp.get('/search')
# def search_flights():
#     origin = request.args.get('origin')
#     destination = request.args.get('destination')
#     passengers = request.args.get('passengers')

#     error = None

#     try:
#         searched_flights = db.session.execute(select(Flight).filter(
#             Flight.origin_city_id == origin, Flight.destination_city_id == destination, Flight.available_seats >= passengers)).scalars().all()
#         for i in searched_flights:
#             print(i)
#     except Exception as e:
#         error = e
#         print(e)
#         abort(500)
#     return render_template('/index.html', flights=search_flights)


def create_seats(flight_id, num_seats):
    error = None
    seats = []
    letters = "ABCDEFGHIJ"
    for i in range(int(num_seats)//10):
        for j in letters:
            seat_number = f'{j}{i+1}'
            seats.append(Seat(flight_id, seat_number))
    try:
        db.session.add_all(i for i in seats)
        db.session.commit()
    except Exception as e:
        error = e
        print(e)
        abort(500)


def delete_seats(flight_id):
    error = None
    try:
        with db.session.no_autoflush:
            db.session.execute(delete(Seat).where(Seat.flight_id == flight_id))

    except Exception as e:
        error = e
        print(e)
        abort(500)


def update_seat(id, flight_id, is_occupied):
    error = None

    try:
        updated_flight = db.session.execute(
            select(Flight).filter(Flight.id == flight_id)).scalar_one()

        print(updated_flight)
        if is_occupied and updated_flight.available_seats > 0:
            updated_flight.available_seats = updated_flight.available_seats-1
        elif not is_occupied and updated_flight.available_seats < 100:
            updated_flight.available_seats = updated_flight.available_seats+1
        db.session.merge(updated_flight)
        print(updated_flight.available_seats)
        db.session.execute(update(Seat).where(
            Seat.id == id).values(is_occupied=is_occupied))
        db.session.commit()
    except Exception as e:
        error = e
        print("in update_seat")
        print(e)
        abort(500)
