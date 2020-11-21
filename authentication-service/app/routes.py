
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import authentication_client as authentication_client
import psycopg2
from . import app
from . import models as models

bp = Blueprint('routes', __name__, url_prefix='/')

#*********************************************************************
# Test
#*********************************************************************
@bp.route('/api/test', methods=['GET', 'POST'])
def test():
    print(request.form)

    name = request.form['the_start']

    print(type(name))

    sample = [
         {'id': 1, 'name': 'test'},
         {'id': 2, 'name': 'test2'},
         {'id': 3, 'name': 'test3'}
    ]

    return json.dumps({'auctions': sample})


#*********************************************************************
# Login
#*********************************************************************
#Login
@bp.route('/api/authentication/login',methods=['POST'])
def login():

     username = request.form.get('username')
     password = request.form.get('password')

     print(request.form)
     
     user = models.Credentials.query.filter(models.Credentials.username.ilike(username)).first()

     if user is None:
          return jsonify({'result': False, 'content': 'User Not Found'})

     if user.password == password:
          success = True
          user.logged_in = True
          models.db.session.commit()
          content = "Success"
     else:
          success = False
          content = 'Incorrect Password'
          
     return jsonify({'result': success, 'content': content})

@bp.route('/api/authentication/logout',methods=['POST'])
def logout():

     username = request.form.get('username')
     
     try:
          user = models.Credentials.query.filter(models.Credentials.username.ilike(username)).first()
          user.logged_in = False
          models.db.session.commit()
          return jsonify({'result': True, 'content': 'Logged Out'})
     except Exception as e:
          return jsonify({'result': False, 'content': 'error'})


@bp.route('/api/authentication/create',methods=['POST'])
def create_credentials():

     print(request.form)

     username = request.form.get('username')
     password = request.form.get('password')

     try:
          new = models.Credentials(username, password, True)
          models.db.session.add(new)
          models.db.session.commit()
          success = True
          content = 'Added'
     except Exception as e:
          success = False
          content = str(e)
          
     return jsonify({'result': True, 'content': content})

@bp.route('/api/authentication/check',methods=['POST'])
def check_login():

     username = request.form.get('username')
     
     user = models.Credentials.query.filter(models.Credentials.username.ilike(username)).first()

     if user is None:
          return jsonify({'result': False, 'content': 'User Not Found'})

     if user.logged_in == True:
          success = True
          content = "Success"
     else:
          success = False
          content = 'Logged out'


     return jsonify({'result': success, 'content': content})
