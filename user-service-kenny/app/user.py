from flask import session
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)
    return db


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine


class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True) # need to make case-insensitive
    email = db.Column(db.String(255), unique=True) # need to make case-insensitive
    address_1 = db.Column(db.String(255))
    address_2 = db.Column(db.String(255))
    address_city = db.Column(db.String(255))
    address_state = db.Column(db.String(2))
    address_zip = db.Column(db.String(5))
    status = db.Column(db.Enum(["active",
                                "suspended",
                                "deleted"]))
    role = db.Column(db.Enum(["basic",
                              "admin"]))

    def __init__(self, username, email, address_1, address_2, address_city,
                 address_state, address_zip, status="active", role="basic"):
        self.username = username
        self.email = email
        self.address_1 = address_1
        self.address_2 = address_2
        self.address_city = address_city
        self.address_state = address_state
        self.address_zip = address_zip
        self.status = status
        self.role = role

    def return_profile(self):
        return self.return_account().update(self.return_address)

    def return_account(self):
        return {
            'username': self.username,
            'email': self.email
            'status': self.status,
            'role': self.role
        }

    def return_address(self):
        return {
            'address_1': self.address_1,
            'address_2': self.address_2,
            'address_city': self.address_city,
            'address_state': self.address_state,
            'address_zip': self.address_zip
        }
