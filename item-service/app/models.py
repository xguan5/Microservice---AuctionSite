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

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique = False, nullable = True)
    description = db.Column(db.String(255),unique = False, nullable = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    flag_id = db.Column(db.Integer, db.ForeignKey('flag.id'))


    def __init__(self,name,description, category_id=None):
        self.name = name
        self.description = description
        self.category_id=category_id

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category_id,
            'flag': self.flag_id

        }

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique = False, nullable = True)
    items = db.relationship('Item')

    def __init__(self,name):
        self.name = name


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255),unique = False, nullable = True)
    items = db.Column(db.Integer)

    def __init__(self,name,items):
        self.name = name
        self.items = items


    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': self.items
        }



