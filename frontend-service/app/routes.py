
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import user_client as users
from . import auction_client as auctions
from . import authentication_client as auth

bp = Blueprint('routes', __name__, url_prefix='/')

def check_login():
    if not session.get('username'): return False
    return auth.check_login(session.get('username'))

#*********************************************************************
# Home, display list of auctions
#*********************************************************************
@bp.route('/', methods=['GET'])
def auction_list():
    print(session)

    if not check_login():
        return redirect( url_for('routes.login') )

    auction_list = auctions.get_all_auctions()

    print(auction_list)

    template = render_template('auction_list.html', 
        auction_list=auction_list
    )
    
    return template

@bp.route('/auction_details/<auction_id>', methods=['GET'])
def get_auction_details(auction_id):

    auction_details = auctions.get_auction_details(auction_id)

    template = render_template('auction_details.html', 
        auction_details=auction_details.get('content')
    )
    
    return template

@bp.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    print(request.form)

    if request.method == 'POST':
        result = auth.login(request.form['username'], request.form['password'])
        print(result)
        if result.get('result') == True:
            session['username'] = request.form['username']
            session['is_admin'] = result['content']
            return redirect(url_for('routes.auction_list'))
        else:
            error = result.get('content')

    template = render_template('login.html', error=error)

    return template

@bp.route('/logout',methods=['POST', 'GET'])
def logout():

     auth.logout(session.get('username'))

     session['username'] = None

     return redirect(url_for('routes.login'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        if request.form['is_admin'] == "TRUE": is_admin = True
        else: is_admin = False


        user_result = users.create_user(request.form)
        credential_result = auth.create_credentials(request.form['username'], request.form['password'], is_admin)

        if user_result.get('result') and credential_result.get('result') == True:
            result = auth.login(request.form['username'], request.form['password'])
            session['username'] = request.form['username']
            session['is_admin'] = is_admin
            return redirect(url_for('routes.auction_list'))
        else:
            if user_result.get('result')  == False:
                error = user_result.get('content')
            if credential_result.get('result')  == False:
                error = credential_result.get('content')

    template = render_template('signup.html', error=error)

    return template


@bp.route('/user-updates/<username>',methods=['POST', 'GET'])
def user_update(username):

    user_details = users.update_user(username, request.form)

    return redirect(url_for('routes.user_details', username=username))
    
@bp.route('/user/<username>',methods=['POST', 'GET'])
def user_details(username):

    if username != session.get('username') and not session.get('is_admin'):
        return "<h1>You are not this user and you are not an admin</h1>"

    user_details = users.get_user_details(username)

    template = render_template('user_details.html', 
        user_details=user_details.get('content')
    )
    
    return template