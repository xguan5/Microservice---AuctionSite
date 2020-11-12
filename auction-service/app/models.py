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
    name = db.Column(db.String(255),unique = False, nullable = False)

    def __init__(self,name):
        self.name = name

    def to_json(self):
        return {
            'name': self.name,
        }

#db.create_all()

# def get_auction_list():

#     return [
#         {
#             'username': 'Tester',
#             'description': 'Filler Texfeaft',
#              'rating': 4.0
#         },
#         {
#             'username': 'Again',
#             'description': 'The ith tije acfioj aoi',
#              'rating': 3.0
#         },
#         {
#             'username': 'Tester',
#             'description': 'Filler Texfeaft',
#              'rating': 5.0
#         }
#     ]
