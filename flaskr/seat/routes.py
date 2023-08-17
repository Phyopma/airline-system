from flask import (
    abort, Blueprint
)

from flaskr.models import Flight, db, Seat
from sqlalchemy import select, delete, update

seat_bp = Blueprint('seats', __name__, url_prefix='/seats')


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
        print(e)
        abort(500)
