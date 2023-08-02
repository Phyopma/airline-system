from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from pydantic import ValidationError


from flaskr.models import Flight

flight_bp = Blueprint('flights', __name__, url_prefix='/flights')


@flight_bp.get('/')
def get_all_flights():
    error = None
    db = get_db()

    flights = db.execute(
        'SELECT * FROM flight'
    ).fetchall()
    return render_template('/index.html', flights=flights)


@flight_bp.post('/new')
def create_airline():
    data = request.form.to_dict()

    db = get_db()
    error = None

    try:
        validated_flight = Flight(**data)
    except ValidationError as e:
        error = e.errors()
        flash(error, "validation")
        return redirect(url_for("flights.get_all_flights"))

    try:
        db.execute("INSERT INTO flight (airline_id, origin_city_id, destination_city_id, total_seats, available_seats, departure_time, duration, price) VALUES (?, ?, ?, ?, ?, ?, ?) ", (validated_flight.airline_id,
                                                                                                                                                                                         validated_flight.origin_city_id, validated_flight.destination_city_id,  validated_flight.total_seats, validated_flight.total_seats, validated_flight.departure_time, validated_flight.duration, validated_flight.price))
        db.commit()
    except:
        abort(500)
    return redirect(url_for("flights.get_all_flights"))


@flight_bp.route('/<int:id>/delete', methods=['POST'])
def delete_flight(id):
    error = None
    db = get_db()

    try:
        db.execute(
            'DELETE FROM airline WHERE id = ?', (id,)
        )

    # db.execute(
    #     'UPDATE user SET role = ? WHERE id = ?',
    #     ('customer', admin_id)
    # )

        db.commit()
    except:
        abort(500)

    return redirect(url_for("flights.get_all_flights"))
