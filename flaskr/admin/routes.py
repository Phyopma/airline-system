from flask import (
    abort, Blueprint, flash, g,  render_template, request, url_for
)

from sqlalchemy import select

from flaskr.models import db, City, AirLine, Flight

from flaskr.auth.routes import login_required, admin_required, super_admin_required

from flaskr.city.routes import get_all_cities

from flaskr.city.routes import get_city_by_id

from flaskr.airline.routes import get_airline_by_id

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.before_request
def get_datas():
    try:
        g.cities = get_all_cities()
        g.airlines = db.session.execute(select(AirLine)).scalars().all()
        g.flights = db.session.execute(select(Flight)).scalars().all()
    except Exception as e:
        abort(500)


@admin_bp.get('/')
@admin_required
def admin_index():
    return render_template('admin/index.html', flights=g.flights, cities=g.cities, airlines=g.airlines, find_city=get_city_by_id, find_airline=get_airline_by_id)
