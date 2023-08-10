from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from sqlalchemy import select, delete

from flaskr.models import Booking, db, User, Flight, AirLine

from flaskr.seat.routes import update_seat, create_seats

from flaskr.auth.routes import login_required, admin_required, super_admin_required
booking_bp = Blueprint('bookings', __name__, url_prefix='/bookings')


@booking_bp.get('/')
@login_required
def get_bookings_for_user():
    error = None
    try:
        bookings = db.session.execute(
            select(Booking).filter(Booking.user_id == g.user.id)).scalars().all()
    except Exception as e:
        error = e
        abort(500)
    flash(error)

    return render_template('/index.html', bookings=bookings)


def get_bookings_by_flight_id(flight_id):
    error = None

    try:
        bookings = db.session.execute(select(Booking).filter(
            Booking.flight_id == flight_id)).scalars().all()
    except Exception as e:
        error = e
        abort(500)
    flash(error)

    return render_template('/index.html', bookings=bookings)


@booking_bp.post('/new')
@login_required
def create_booking():
    data = request.form.to_dict()

    data['user_id'] = g.user.id
    flight_id = data['flight_id']
    seat_id = data['seat_id']
    error = None

    try:
        new_booking = Booking(**data)
        db.session.add(new_booking)
        update_seat(seat_id, flight_id, True)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)
    return redirect(url_for("bookings.get_bookings_for_user"))


@booking_bp.route('/<int:booking_id>/delete', methods=['POST'])
@login_required
# admin or super_admin
def delete_booking(booking_id):
    error = None

    try:
        db.session.execute(delete(Booking).where(Booking.id == booking_id))
        db.session.commit()

    except Exception as e:
        error = e
        print(e)
        abort(500)

    return redirect(url_for("bookings.get_bookings_for_user"))
