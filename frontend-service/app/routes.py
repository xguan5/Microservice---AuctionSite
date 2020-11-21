
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

#*********************************************************************
# Home, display list of auctions
#*********************************************************************
@bp.route('/', methods=['GET'])
def auction_list():

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
        auction_details=auction_details.get('result')
    )
    
    return template

@bp.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':
        result = auth.login(request.form['user_id'], request.form['password'])

        print(result)
        if result.get('result') == True:
            return redirect(url_for('routes.auction_list'))
        else:
            error = result.get('message')

    template = render_template('login.html', error=error)

    return template

#*********************************************************************
# Display list of users
#*********************************************************************
@bp.route('/user_list', methods=['GET'])
def user_list():  

    user_list = users.get_user_list()


    template = render_template('user_list.html', 
        user_list=user_list
    )

    return template