from flask import Flask
from models import db

app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    SQLALCHEMY_DATABASE_URI='postgresql://localhost/pmt_db' ))

db.init_app(app)