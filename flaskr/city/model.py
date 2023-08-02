from flask_sqlalchemy import SQLAlchemy
from flaskr.db import get_db
import sqlalchemy as sa

db = get_db()


class City(db.Model):
    id = db.Column(sa.Integer, primary_key=True, unique=True)
    name = db.Column(sa.String(40))
