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
    status = db.Column(db.String(10))

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

    def return_profile(self):
        return {
            'username': self.username,
            'email': self.email,
            'status': self.status,
            'address_1': self.address_1,
            'address_2': self.address_2,
            'address_city': self.address_city,
            'address_state': self.address_state,
            'address_zip': self.address_zip
        }

    def return_account(self):
        return {
            'username': self.username,
            'email': self.email,
            'status': self.status
        }

    def return_address(self):
        return {
            'address_1': self.address_1,
            'address_2': self.address_2,
            'address_city': self.address_city,
            'address_state': self.address_state,
            'address_zip': self.address_zip
        }


class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    rater_id = db.Column(db.String(255))
    recipient_id = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    review = db.Column(db.String(4000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, rating_id, rater_id, recipient_id, rating, review, timestamp):
        self.rating_id = rating_id
        self.rater_id = rater_id
        self.recipient_id = recipient_id
        self.rating = rating
        self.review = review
        self.timestamp = timestamp

    def return_rating(self):
        return {
            'rater_id': self.rater_id,
            'recipient_id': self.recipient_id,
            'rating': self.rating,
            'review': self.review,
            'timestamp': self.timestamp
        }


class CartItem(db.Model):
    username = db.Column(db.String(255), unique=True)
    auc_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username, auc_id):
        self.username = username
        self.auc_id = auc_id

    def return_cart_item(self):
        return {
            'user_id': self.username,
            'auc_id': self.auc_id
        }


class WatchlistItem(db.Model):
    username = db.Column(db.String(255), unique=True)
    auc_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, username, auc_id):
        self.username = username
        self.auc_id = auc_id

    def return_watchlist_item(self):
        return {
            'user_id': self.username,
            'auc_id': self.auc_id
        }
