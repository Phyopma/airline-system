import os

from flask import Flask, render_template
from flaskr.auth.routes import auth_bp
from flaskr.super_admin.routes import super_admin_bp
from flaskr.flight.routes import flight_bp
from flaskr.city.routes import city_bp


def internal_server_error(e):
    return render_template('500.html'), 500


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(super_admin_bp)
    app.register_blueprint(flight_bp)
    app.register_blueprint(city_bp)
    app.register_error_handler(500, internal_server_error)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
