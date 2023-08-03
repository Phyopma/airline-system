from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from sqlalchemy import select

from pydantic import ValidationError

from flaskr.models import db, City

city_bp = Blueprint('cities', __name__, url_prefix='/cities')


@city_bp.get('/')
def get_all_cities():
    error = None
    cities = db.session.execute(select(City))
    return render_template('/index.html', cities=cities)


@city_bp.post('/new')
def create_city():
    data = request.form.to_dict()
    error = None
    try:
        new_city = City(**data)
        db.session.add(new_city)
        db.session.commit()
    except Exception as e:
        print("errors", e)
        abort(500)
    return redirect(url_for("cities.get_all_cities"))


@city_bp.route('/<int:id>/delete', methods=['POST'])
def delete_city(id):
    error = None

    try:
        db.session.delete(db.get_or_404(City, id))
        db.session.commit()

    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("cities.get_all_cities"))