from flask import session
import requests
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from flask_marshmallow import Marshmallow

db = SQLAlchemy()
#ma = Marshmallow()

def init_app(app):
    db.app = app
    db.init_app(app)
    #ma.app = app
    #ma.init_app(app)
    return db


def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

class Auction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique = False, nullable = True)
    buy_now_price = db.Column(db.Float)
    start_bid_price = db.Column(db.Float)
    inc_bid_price = db.Column(db.Float)
    status = db.Column(db.String(50), default="Draft")
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, onupdate = datetime.utcnow)
    creator_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    winner_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    biddings = db.relationship('Bidding')



    def __init__(self,name,buy_now_price,start_bid_price,inc_bid_price,start_time,end_time,creator_id,item_id):
        self.name = name
        self.buy_now_price = buy_now_price
        self.start_bid_price = start_bid_price
        self.inc_bid_price = inc_bid_price
        self.start_time = start_time
        self.end_time = end_time
        self.creator_id = creator_id
        self.item_id = item_id

    def to_json(self):
        return {
            'name': self.name,
            'creator': self.creator_id,
            'item': self.item_id,
            'buy_now_price': self.buy_now_price,
            'start_bid_price': self.start_bid_price,
            'inc_bid_price': self.inc_bid_price,
            'start_time': self.start_time,
            'end_time': self.end_time
        }

class Bidding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id') )
    bid_price = db.Column(db.Float)
    bid_placed = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,user_id,auction_id,bid_price,bid_placed):
        self.user_id = user_id
        self.auction_id = auction_id
        self.bid_price = bid_price
        self.bid_placed = bid_placed

    def to_json(self):
        return {
            'user': self.user_id,
            'auction': self.auction_id,
            'bid_price': self.bid_price,
            'bid_placed': self.bid_placed
        }