
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import user_client as users

bp = Blueprint('routes', __name__, url_prefix='/')

#*********************************************************************
# Home, display list of auctions
#*********************************************************************
@bp.route('/', methods=['GET'])
def auction_list():

    print('here')
    
    auction_list = [
        {
            'title': 'iPhone 16s',
            'description': 'Phone from the future in mint condition',
            'current_bid': '$80.53',
            'buy_now_price': '499.99'

        },
        {
            'title': 'Golden Retriever',
            'description': 'Who put a dog on here? that\'s kind of messed up.',
            'current_bid': '$999.53',
            'buy_now_price': '10000000.99'
        }
    ]

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