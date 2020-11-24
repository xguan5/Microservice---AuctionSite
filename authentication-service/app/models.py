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
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    db.metadata.create_all(engine)
    return engine

class Credentials(db.Model):
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    logged_in = db.Column(db.Boolean)
    is_admin = db.Column(db.Boolean)

    #auction_id = db.Column(db.Integer, db.ForeignKey('auction.id') )
    #bid_placed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,username,password, logged_in=False, is_admin=False):
        self.username = username
        self.password = password
        self.logged_in = logged_in
        self.is_admin = is_admin

    def to_json(self):
        return {
            'username': self.username,
            'password': self.password,
            'logged_in': self.logged_in,
            'is_admin': self.is_admin
        }