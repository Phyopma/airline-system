from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from datetime import datetime
from flaskr.models import db, User, AirLine
from sqlalchemy import select, update, delete

super_admin_bp = Blueprint('super-admin', __name__, url_prefix='/super-admin')


@super_admin_bp.route('/airlines', methods=["GET"])
def get_all_airlines():
    error = None

    airlines = db.session.execute(select(AirLine)).scalars().all()

    return render_template('super_admin/airlines/index.html', airlines=airlines)


@super_admin_bp.route('/airlines/new', methods=['POST'])
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
            return redirect(url_for("super-admin.get_all_airlines"))

    flash(error)

    return redirect(url_for("super-admin.get_all_airlines"))


@super_admin_bp.route('/airlines/<int:id>/delete', methods=['POST'])
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

    return redirect(url_for("super-admin.get_all_airlines"))
