from pydantic import BaseModel
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa


db = SQLAlchemy()


class City_create(BaseModel):
    name: str


class City(db.Model):
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    name = sa.Column(sa.String(40))
