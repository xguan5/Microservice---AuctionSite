from flask import Flask, make_response, abort, request, session, g, redirect, \
    redirect, url_for, abort, render_template, flash, escape, json, jsonify,\
        Response, Blueprint
from models import db, PaymentMethod, Trasaction
from datetime import datetime
import os
import sys
import traceback


bp = Blueprint('routes', __name__, url_prefix='/')

# create shipping label
@bp.route('/api/delivery/generatelabel', methods=['POST'])
def create_label(userid):
	pass

# create a delivery
@bp.route('api/delivery/create',methods=['POST'])
def schedule_delivery():
	pass
