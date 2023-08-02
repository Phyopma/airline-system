from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, url_for
)


from pydantic import ValidationError

from flaskr.db import get_db

from flaskr.city.model import City

city_bp = Blueprint('cities', __name__, url_prefix='/cities')


@city_bp.get('/')
def get_all_cities():
    error = None
    db = get_db()

    # cities = db.execute(
    #     'SELECT * FROM city'
    # return render_template('/index.html', cities=cities)
    cities = db.session.execute(db.select(City))
    print(cities)
    return render_template('/index.html', cities=cities)


# @city_bp.post('/new')
# def create_city():
#     data = request.form.to_dict()

#     db = get_db()
#     error = None

#     try:
#         validated_city = City_create(**data)
#     except ValidationError as e:
#         error = e.errors()
#         flash(error, "validation")
#         return redirect(url_for("cities.get_all_cities"))

#     try:
#         db.execute("INSERT INTO city (name,) VALUES (?,)",
#                    (validated_city,))
#         db.commit()
#     except Exception as e:
#         abort(500)
#     return redirect(url_for("cities.get_all_cities"))


# @city_bp.route('/<int:id>/delete', methods=['POST'])
# def delete_city(id):
#     error = None
#     db = get_db()

#     try:
#         db.execute(
#             'DELETE FROM city WHERE id = ?', (id,)
#         )

#     # db.execute(
#     #     'UPDATE user SET role = ? WHERE id = ?',
#     #     ('customer', admin_id)
#     # )

#         db.commit()
#     except:
#         abort(500)

#     return redirect(url_for("cities.get_all_cities"))
