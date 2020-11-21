
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

     user_id = request.form.get('user_id')
     password = request.form.get('password')

     print(request.form)
     
     user = models.Credentials.query.filter(models.Credentials.user_id.ilike(user_id)).first()

     if user is None:
          return jsonify({'result': False, 'message': 'User Not Found'})

     if user.password == password:
          success = True
          message = "Success"
     else:
          success = False
          message = 'Incorrect Password'
          
     return jsonify({'result': success, 'message': message})

@bp.route('/api/authentication/check_login',methods=['POST'])
def login():

     user_id = request.form.get('user_id')
     
     result = True#check_login(user_id)

     return jsonify(result)