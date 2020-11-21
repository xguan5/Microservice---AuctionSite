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

class delivery(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tracking_num = db.Column(db.Integer)
    courier = db.Column(db.String(5), nullable = False)
    shipping_option = db.Column(db.String(10), nullable = False)
    
    def __init__(self, transact_id, courier, shipping_option):
        self.transact_id = transact_id
        self.courier = courier
        self.shipping_option = shipping_option
        
        self.tracking_num = 0

    def to_json(self):
        return {
            'transact_id': self.transact_id,
            'courier': self.courier,
            'shipping_option': self.shipping_option,
            'billing_address2':self.billing_address2,
            'tracking_num':self.tracking_num
        }

