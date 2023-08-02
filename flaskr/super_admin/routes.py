from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)


super_admin_bp = Blueprint('super-admin', __name__, url_prefix='/super-admin')


@super_admin_bp.route('/airlines', methods=["GET"])
def get_all_airlines():
    error = None
    db = get_db()

    airlines = db.execute(
        'SELECT * FROM airline'
    ).fetchall()

    return render_template('super_admin/airlines/index.html', airlines=airlines)


@super_admin_bp.route('/airlines/new', methods=['POST'])
def create_airline():
    airline_name = request.form['airline_name']
    email = request.form['email']

    error = None
    db = get_db()

    if not airline_name:
        error = 'Airline Name is required.'
    elif not email:
        error = 'Email is required.'

    user = db.execute(
        'SELECT * FROM user WHERE email = ?', (email,)
    ).fetchone()

    if user is None:
        error = 'Sorry, couldn\'t find any user with this email.'

    if error is None:
        try:
            db.execute(
                "INSERT INTO airline (name, admin_id) VALUES (?, ?)",
                (airline_name, user['id']),
            )

            db.execute(
                'UPDATE user SET role = ? WHERE id = ?',
                ('admin', user['id'])
            )

            db.commit()
        except db.IntegrityError:
            error = "Error when creating airline"
        else:
            return redirect(url_for("super-admin.get_all_airlines"))

    flash(error)

    return redirect(url_for("super-admin.get_all_airlines"))


@super_admin_bp.route('/airlines/<int:id>/delete', methods=['POST'])
def delete_airline(id):
    error = None
    db = get_db()

    admin_id = db.execute(
        'SELECT admin_id FROM airline WHERE id = ?', (id,)
    ).fetchone()['admin_id']

    db.execute(
        'DELETE FROM airline WHERE id = ?', (id,)
    )

    db.execute(
        'UPDATE user SET role = ? WHERE id = ?',
        ('customer', admin_id)
    )

    db.commit()

    return redirect(url_for("super-admin.get_all_airlines"))
