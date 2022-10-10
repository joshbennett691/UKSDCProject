from flask_login import UserMixin

from init_db import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(0), nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Following(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_no = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)