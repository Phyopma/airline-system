from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from flaskr.models import db, User, AirLine
from sqlalchemy import select, update, delete
from flaskr.auth.routes import super_admin_required, admin_required, login_required

airline_bp = Blueprint('airlines', __name__, url_prefix='/airlines')


@airline_bp.route('/', methods=["GET"])
# @super_admin_required
def get_all_airlines():
    error = None

    airlines = db.session.execute(select(AirLine)).scalars().all()

    return render_template('airlines/index.html', airlines=airlines)


@airline_bp.route('/new', methods=['POST'])
# @super_admin_required
def create_airline():
    airline_name = request.form['airline_name']
    email = request.form['email']
    error = None

    if not airline_name:
        error = 'Airline Name is required.'
    elif not email:
        error = 'Email is required.'

    # user = db.execute(
    #     'SELECT * FROM user WHERE email = ?', (email,)
    # ).fetchone()

    user = db.first_or_404(select(User).filter(User.email == email))
    print("User", user)
    if user is None:
        error = 'Sorry, couldn\'t find any user with this email.'

    if error is None:
        try:
            db.session.add(AirLine(user.id, airline_name))

            db.session.execute(update(User).where(
                User.id == user.id).values(role='admin'))

            db.session.commit()

        except db.IntegrityError as e:
            print(e)
            error = "Error when creating airline"
        else:
            return redirect(url_for("airlines.get_all_airlines"))

    flash(error)

    return redirect(url_for("airlines.get_all_airlines"))


@airline_bp.route('/<int:id>/delete', methods=['POST'])
@super_admin_required
def delete_airline(id):
    error = None

    try:
        admin_id = db.first_or_404(
            select(AirLine.admin_id).filter(AirLine.id == id))

        db.session.execute(delete(AirLine).filter(AirLine.id == id))

        db.session.execute(update(User).where(
            User.id == admin_id).values(role='customer'))

        db.session.commit()
    except Exception as e:
        db.session.flush()
        error = e

    flash(error)

    return redirect(url_for("airlines.get_all_airlines"))
