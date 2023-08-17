from flask import (
    abort, Blueprint, flash, g,  render_template, request, url_for
)
from sqlalchemy import select
from flaskr.models import db, City, AirLine, Flight
from flaskr.auth.routes import login_required, admin_required, super_admin_required
from flaskr.city.routes import get_all_cities
from flaskr.airline.routes import get_airline_by_admin_id
from flaskr.flight.routes import get_flights_by_airline_id

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def get_datas():
    try:
        g.cities = get_all_cities()
    except Exception as e:
        abort(500)


@admin_bp.get('/')
@admin_required
def admin_index():
    airline = get_airline_by_admin_id()
    flights = get_flights_by_airline_id(airline.id)
    return render_template('admin/index.html', flights=flights, cities=g.cities, airline=airline)
