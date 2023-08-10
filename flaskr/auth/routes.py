import functools

from flask import (
    abort, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.models import User, db
from sqlalchemy import select


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        data = request.form.to_dict()
        if (data['password'] == data['re-password']):
            data['password'] = generate_password_hash(data['password'])
        else:
            error = "Passwords need to be same!!"
        data.pop('re-password')

        print(data)

        if error == None:
            try:
                new_user = User(**data)
                db.session.add(new_user)
                db.session.commit()
            except db.IntegrityError as e:
                print(e)
                error = f"User {data['email']} is already registered."
                return redirect(url_for("auth.register"))

    return render_template('auth/register.html', error=error)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = db.first_or_404(
            select(User).filter(User.email == data['email']))
        # user = db.get_or_404(User, {"email": data['email']})
        print(user.email)
        error = None
        if user is None:
            error = 'Incorrect Email.'
        elif not check_password_hash(user.password, data['password']):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
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


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user.role == 'customer':
            abort(401)
        return view(**kwargs)
    return wrapped_view


def super_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user.role != 'super-admin':
            abort(401)
        return view(**kwargs)
    return wrapped_view
