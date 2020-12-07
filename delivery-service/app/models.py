from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import random

db = SQLAlchemy()

def init_app(app):
    db.app = app
    db.init_app(app)
    return db

def create_tables(app):
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    db.metadata.create_all(engine)
    return engine

class delivery(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pacakage_size = db.Column(db.String, nullable = False)
    tracking_num = db.Column(db.Integer)
    courier = db.Column(db.String(5), nullable = False)
    shipping_option = db.Column(db.String(10), nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)

    seller_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    seller_name = db.Column(db.String(26), nullable = False)
    seller_address1 = db.Column(db.String(50), nullable = False)
    seller_address2 = db.Column(db.String(10))
    seller_city = db.Column(db.String(20), nullable = False)
    seller_state = db.Column(db.String(2), nullable = False)
    seller_zip = db.Column(db.Integer, nullable = False)

    buyer_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    buyer_name = db.Column(db.String(26), nullable = False)
    buyer_address1 = db.Column(db.String(50), nullable = False)
    buyer_address2 = db.Column(db.String(10))
    buyer_city = db.Column(db.String(20), nullable = False)
    buyer_state = db.Column(db.String(2), nullable = False)
    buyer_zip = db.Column(db.Integer, nullable = False)

    def __init__(self, transact_id, package_size, courier, shipping_option, \
        seller_name, seller_address1, seller_address2, seller_city, seller_state, seller_zip,\
            buyer_name, buyer_address1, buyer_address2, buyer_city, buyer_state, buyer_zip  ):
        self.transact_id = transact_id
        self.package_size = package_size
        self.courier = courier
        self.shipping_option = shipping_option
        self.tracking_num = 0

    def shipping_label(self):
        return {
            'from_name': self.seller_name,
            'from_address1': self.seller_address1, 
            'from_address2': self.seller_address2, 
            'from_city': self.seller_city, 
            'from_state': self.seller_state,
            'from_zip': self.seller_zip,
            'to_name': self.buyer_name,
            'to_address1': self.buyer_address1, 
            'to_address2': self.buyer_address2, 
            'to_city': self.buyer_city, 
            'to_state': self.buyer_state,
            'to_zip': self.buyer_zip,
            'tracking_num': self.tracking_num
        }
    
    def return_label(self):
        return {
            'from_name': self.buyer_name,
            'from_address1': self.buyer_address1, 
            'from_address2': self.buyer_address2, 
            'from_city': self.buyer_city, 
            'from_state': self.buyer_state,
            'from_zip': self.buyer_zip,
            'to_name': self.seller_name,
            'to_address1': self.seller_address1, 
            'to_address2': self.seller_address2, 
            'to_city': self.seller_city, 
            'to_state': self.seller_state,
            'to_zip': self.seller_zip,
            'tracking_num': self.tracking_num
        }
    
    def get_tracking(self):
        return {
            'timestamp': self.timestamp,
            'tracking_num': self.tracking_num,
            'estimated_delivery': '5-7 days from timestamp'
        }

    def to_json(self):
        return {
            'transact_id': self.transact_id,
            'courier': self.courier,
            'shipping_option': self.shipping_option,
            'billing_address2':self.billing_address2,
            'tracking_num':self.tracking_num
        }

