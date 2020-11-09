
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import user_client as user_client

bp = Blueprint('routes', __name__, url_prefix='/')

#*********************************************************************
# Return a list of all users
#*********************************************************************
@bp.route('/api/user_list', methods=['GET'])
def user_list():
    
    user_list = user_client.get_user_list()

    print(json.dumps(user_list))

    return json.dumps(user_list)
