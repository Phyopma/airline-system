from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from flaskr.seat.routes import create_seats, delete_seats


from flaskr.models import Flight, db, City

from sqlalchemy import select, insert, delete


flight_bp = Blueprint('flights', __name__, url_prefix='/flights')


@flight_bp.get('/')
def get_all_flights():
    error = None

    try:
        flights = db.session.execute(select(Flight))
    except Exception as e:
        print(e)
        abort(500)

    return render_template('/index.html', flights=flights)


@flight_bp.get('/<int:airline_id>/')
def get_flights_by_airline_id(airline_id):
    error = None

    try:
        flights = db.session.execute(
            select(Flight).filter_by(airline_id=airline_id))
    except Exception as e:
        print(e)
        abort(500)

    return render_template('/index.html', flights=flights)


@flight_bp.get('/search')
def search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    passengers = request.args.get('passengers')

    error = None

    try:
        searched_flights = db.session.execute(select(Flight).filter(
            Flight.origin_city_id == origin, Flight.destination_city_id == destination, Flight.available_seats >= passengers)).scalars().all()
    except Exception as e:
        error = e
        print(e)
        abort(500)
    return render_template('/index.html', flights=search_flights)


@flight_bp.post('/new')
def create_flight():
    data = request.form.to_dict()
    data['available_seats'] = data['total_seats']
    data['departure_time'] = datetime(2024, 12, 10, 5, 30)
    error = None

    try:
        new_flight = Flight(**data)
        db.session.add(new_flight)
        db.session.commit()
        # print(new_flight.id)
        create_seats(new_flight.id, new_flight.total_seats)

    except Exception as e:
        print(e)
        abort(500)
    return redirect(url_for("flights.get_all_flights"))


@flight_bp.route('/<int:id>/delete', methods=['POST'])
def delete_flight(id):
    error = None

    try:
        flight = db.get_or_404(Flight, id)
        db.session.delete(flight)
        delete_seats(id)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("flights.get_all_flights"))
