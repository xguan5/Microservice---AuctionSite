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


class Email(db.Model):
    e_id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255))
    recipient = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    msg = db.Column(db.String(20000))
    needs_reply = db.Column(db.Boolean, default=True)

    def __init__(self, e_id, sender, recipient, subject, msg, needs_reply):
        self.e_id = e_id
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.msg = msg
        self.needs_reply = needs_reply

    def return_email(self):
        return {
            'e_id': self.e_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'subject': self.subject,
            'message': self.msg,
            'needs_reply': self.needs_reply
        }
