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

class PaymentMethod(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    billing_name = db.Column(db.String(26), nullable = False)
    billing_address1 = db.Column(db.String(50), nullable = False)
    billing_address2 = db.Column(db.String(10))
    billing_city = db.Column(db.String(20), nullable = False)
    billing_zip = db.Column(db.Integer, nullable = False)
    billing_state = db.Column(db.String(2), nullable = False)
    billing_country = db.Column(db.String(2), nullable = False)
    exp_date = db.Column(db.Integer, nullable = False)
    csv_code = db.Column(db.Integer, nullable = False)
    
    def __init__(self, user_id, billing_name, billing_address1, \
        billing_address2, billing_city, billing_zip, billing_state, \
            billing_country, exp_date, csv_code):
        self.billing_name = billing_name
        self.billing_address1 = billing_address1
        self.billing_address2 = billing_address2
        self.billing_city = billing_city
        self.billing_zip = billing_zip
        self.billing_state = billing_state
        self.billing_country = billing_country
        self.exp_date = exp_date
        self.csv_code = csv_code

    def update_method(self):
        pass

    def remove_method(self):
        pass

    def to_json(self):
        return {
            'billing_name': self.billing_name,
            'billing_address1': self.billing_address1,
            'billing_address2':self.billing_address2,
            'billing_city': self.billing_city,
            'billing_zip': self.billing_zip,
            'billing_state': self.sbilling_state,
            'billing_country':self.billing_country,
            'exp_date':self.exp_date
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    # Need to confirm if the following foreign keys are consistent
    payer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Assuming a transaction can have multiple auctions checked out together
    auctions = db.relationship('CheckoutAuction', backref='checkoutAction')
    transact_date = db.Column(db.DateTime, default = datetime.utcnow)
    auction

    def to_json(self):
        return {
            'payer_id': self.payer_id,
            'receiver_id': self.receiver_id
            'auctions':self.auctions
            'transact_date': self.transact_date
        }

class CheckoutAuction(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    auction_id = db.Column(db.Integer, db.ForeignKey('auction.id'))
    item_id = deb.Column(db.Integer, db.ForeignKey('item.id'))
    
