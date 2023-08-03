from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)

from sqlalchemy import select

from pydantic import ValidationError

from flaskr.db import db_session

from flaskr.models import City

city_bp = Blueprint('cities', __name__, url_prefix='/cities')


@city_bp.get('/')
def get_all_cities():
    error = None

    cities = db_session.execute(select(City))
    return render_template('/index.html', cities=cities)


@city_bp.post('/new')
def create_city():
    data = request.form.to_dict()
    error = None
    try:
        new_city = City(**data)
        db_session.add(new_city)
        db_session.commit()
    except Exception as e:
        print("errors", e)
        abort(500)
    return redirect(url_for("cities.get_all_cities"))


@city_bp.route('/<int:id>/delete', methods=['POST'])
def delete_city(id):
    error = None

    try:

        db_session.delete(db_session.get(City, id))
        db_session.commit()

    except Exception as e:
        print(e)
        abort(500)

    return redirect(url_for("cities.get_all_cities"))
