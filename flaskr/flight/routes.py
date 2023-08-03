from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from pydantic import ValidationError


from flaskr.models import Flight, db

from sqlalchemy import select


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


@flight_bp.post('/new')
def create_airline():
    data = request.form.to_dict()
    data['available_seats'] = data['total_seats']
    data['departure_time'] = datetime(2024, 12, 10, 5, 30)
    error = None

    try:
        new_flight = Flight(**data)
        db.session.add(new_flight)
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500)
    return redirect(url_for("flights.get_all_flights"))


@flight_bp.route('/<int:id>/delete', methods=['POST'])
def delete_flight(id):
    error = None

    try:
        flight = db.get_or_404(Flight, id)
        db.session.delete(flight_bp)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("flights.get_all_flights"))
