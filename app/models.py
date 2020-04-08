import enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)

# class Attraction(db.Model):
#     __tablename__ = "attractions"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128), nullable=False)
#     rating = db.Column(db.Float, nullable=False)
#     latitude = db.Column(db.Float, nullable=False)
#     longitude = db.Column(db.Float, nullable=False)

# class ViewType(enum.Enum):
#     RESTAURANT = "restaurant"
#     ATTRACTION = "attraction"

# class UserPreference(db.Model):
#     __tablename__ = "user_preferences"
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), primary_key=True)
#     type = db.Column(db.Enum(ViewType), nullable=False)
#     item_id = db.Column(db.Integer, nullable=False, primary_key=True)
