from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from datetime import datetime

from flaskr.seat.routes import create_seats, delete_seats

from flaskr.auth.routes import login_required, admin_required, super_admin_required

from flaskr.city.routes import get_all_cities

from flaskr.airline.routes import get_all_airlines

from flaskr.models import Flight, db, City, AirLine

from flaskr.city.routes import get_city_by_id

from flaskr.airline.routes import get_airline_by_id

from sqlalchemy import select, insert, delete


flight_bp = Blueprint('flights', __name__, url_prefix='/flights')


@flight_bp.before_request
def get_datas():
    try:
        g.cities = get_all_cities()
        g.airlines = db.session.execute(select(AirLine)).scalars().all()
        g.flights = db.session.execute(select(Flight)).scalars().all()
    except Exception as e:
        abort(500)


@flight_bp.get('/')
def get_all_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    num_seats = request.args.get('num_seats')
    departure_time_from_input = request.args.get('departure_time')

    tmp_date = departure_time_from_input.replace(
        'T', '-').replace(':', '-').split('-')
    year, month, day, hour, minute = map(int, tmp_date)
    departure_time = datetime(
        year, month, day, hour, minute)
    error = None
    try:
        searched_flights = db.session.execute(select(Flight).filter(
            Flight.origin_city_id == origin, Flight.destination_city_id == destination, Flight.available_seats >= num_seats, Flight.departure_time >= departure_time,  Flight.departure_time >= departure_time)).scalars().all()
    except Exception as e:
        error = e
        print(e)
        abort(500)

    return render_template('/flights/index.html', flights=searched_flights, cities=g.cities,  find_city=get_city_by_id, find_airline=get_airline_by_id, airlines=g.airlines)


# @flight_bp.get('/')
# def get_flights_by_airline_id():
#     error = None
#     airline_id = request.args.get('airline_id')
#     try:
#         if airline_id:
#             flights = db.session.execute(
#                 select(Flight).filter_by(airline_id=airline_id)).scalars().all()
#         else:
#             flights = db.session.execute(select(Flight)).scalars().all()
#         print(flights)
#     except Exception as e:
#         print(e)
#         abort(500)

#     return render_template('flights/index.html', flights=flights)


@flight_bp.post('/search')
def search_flights():
    searched_flights = []
    # referrer = request.referrer
    data = request.form.to_dict()
    tmp_date = data['departure_time'].replace(
        'T', '-').replace(':', '-').split('-')
    year, month, day, hour, minute = map(int, tmp_date)
    data['departure_time'] = datetime(
        year, month, day, hour, minute)
    error = None
    try:
        searched_flights = db.session.execute(select(Flight).filter(
            Flight.origin_city_id == data['origin'], Flight.destination_city_id == data['destination'], Flight.available_seats >= data['num_seats'], Flight.departure_time >= data['departure_time'],  Flight.departure_time >= data['departure_time'])).scalars().all()
    except Exception as e:
        error = e
        print(e)
        abort(500)
# if referrer and not request.path in referrer:
#     return redirect(referrer)
# else:
    return redirect(url_for('flights.get_all_flights', flights=searched_flights, cities=g.cities,  find_city=get_city_by_id, find_airline=get_airline_by_id, airlines=g.airlines))


@flight_bp.post('/new')
@admin_required
def create_flight():
    data = request.form.to_dict()
    print("in_flight_create", data)
    data['airline_id'] = db.first_or_404(
        select(AirLine.id).filter(AirLine.admin_id == g.user.id))
    tmp_date = data['departure_time'].replace(
        'T', '-').replace(':', '-').split('-')
    year, month, day, hour, minute = map(int, tmp_date)
    data['departure_time'] = datetime(
        year, month, day, hour, minute)
    tmp_date = data['arrival_time'].replace(
        'T', '-').replace(':', '-').split('-')
    year, month, day, hour, minute = map(int, tmp_date)
    data['arrival_time'] = datetime(
        year, month, day, hour, minute)

    data['available_seats'] = data['total_seats']
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
    if request.referrer and not request.path in request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for("flights.get_all_flights"))


@flight_bp.route('/<int:id>/delete', methods=['POST'])
# @admin_required
def delete_flight(id):
    error = None

    try:
        # airline_id = db.first_or_404(
        #     select(AirLine.id).filter(AirLine.admin_id == g.user.id))
        flight = db.get_or_404(Flight, id)
        # if (flight.airline_id != airline_id):
        #     abort(401)
        db.session.delete(flight)
        delete_seats(id)
        db.session.commit()
    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("flights.get_all_flights"))
