from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from sqlalchemy import select


from flaskr.auth.routes import login_required, super_admin_required

from flaskr.models import db, AirLine, City

super_admin_bp = Blueprint('super-admin', __name__, url_prefix='/super-admin')


@super_admin_bp.get('/')
# @admin_required
def super_admin_index():
    airlines = db.session.execute(select(AirLine)).scalars().all()
    cities = db.session.execute(select(City)).scalars().all()
    return render_template('super-admin/index.html', airlines=airlines, cities=cities)
