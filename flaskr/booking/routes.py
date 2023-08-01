from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from pydantic import ValidationError

from flaskr.db import get_db

from flaskr.booking.booking_model import Booking

booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@booking_bp.get('/')
def get_all_bookings():
    error = None
    db = get_db()

    bookings = db.execute(
        'SELECT * FROM booking'
    ).fetchall()
    return render_template('/index.html', bookings=bookings)


@booking_bp.post('/new')
def create_airline():
    data = request.form.to_dict()

    db = get_db()
    error = None

    try:
        validated_booking = Booking(**data)
    except ValidationError as e:
        error = e.errors()
        flash(error, "validation")
        return redirect(url_for("bookings.get_all_bookings"))

    try:
        db.execute(
            "INSERT INTO booking (passenger_id, flight_id, seat_id, booked_at) VALUES (?, ?, ?, ? ) ", (validated_booking))
        db.commit()
    except:
        abort(500)
    return redirect(url_for("bookings.get_all_bookings"))


@booking_bp.route('/<int:id>/delete', methods=['POST'])
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

    return redirect(url_for("bookings.get_all_bookings"))
