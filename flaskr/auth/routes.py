import functools

from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import User, db


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()

        data['password'] = generate_password_hash(data['password'])
        error = None
        try:
            new_user = User(**data)
            db.session.add(User)
            db.session.commit()
        except db.IntegrityError:
            error = f"User {data['email']} is already registered."
            return redirect(url_for("auth.register"))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = db.get_or_404(User, {"email": data['email']})
        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user['password'], data['password']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        else:
            abort(400, error)

    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:

        g.user = db.get_or_404(User, user_id)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
