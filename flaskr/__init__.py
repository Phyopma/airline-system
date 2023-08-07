from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import click


def internal_server_error(e):
    return render_template('500.html'), 500


def authorization_error(e):
    return render_template('401.html'), 401


app = Flask(__name__, instance_relative_config=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.secret_key = 'gg_project'

with app.app_context():
    from flaskr.models import db
    from flaskr.auth.routes import auth_bp
    from flaskr.super_admin.routes import super_admin_bp
    from flaskr.flight.routes import flight_bp
    from flaskr.city.routes import city_bp
    from flaskr.booking.routes import booking_bp
    db.create_all()

# if test_config is None:
#     app.config.from_pyfile('config.py', silent=True)
# else:
# app.config.from_mapping(test_config)

# try:
#     os.makedirs(app.instance_path)
# except OSError:
#     pass


app.register_blueprint(auth_bp)
app.register_blueprint(super_admin_bp)
app.register_blueprint(flight_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(city_bp)
app.register_error_handler(401, authorization_error)
app.register_error_handler(500, internal_server_error)
# app.cli.add_command(init_db_command)


@app.route("/")
def index():
    return render_template('index.html')


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.flush()


@click.command('init-db')
def refresh_db():
    """Clear the existing data and create new tables."""
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')


app.cli.add_command(refresh_db)
