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
def create_label(transact_id):
    pass

# create a delivery
@bp.route('api/delivery/create',methods=['POST'])
def schedule_delivery(transaction_id):
	new_info = request.form
	package_size = new_info['package_size'] # small package or med / large boxes
    courier = new_info['courier'] # DHL, EMS, Fedex
    shipping_option = new_info['shipping_option'] # standard or expedited

    Delivery(transact_id, package_size, courier, shipping_option))
    
    return True
    
