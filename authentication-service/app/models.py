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
    user_id = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    #auction_id = db.Column(db.Integer, db.ForeignKey('auction.id') )
    #bid_placed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,user_id,password):
        self.user_id = user_id
        self.password = password

    def to_json(self):
        return {
            'user': self.user_id,
            'password': self.password
        }