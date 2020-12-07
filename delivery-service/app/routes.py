from flask import Flask, make_response, abort, request, session, g, redirect, \
    redirect, url_for, abort, render_template, flash, escape, json, jsonify,\
        Response, Blueprint
from . import models
from datetime import datetime
import os
import sys
import traceback


bp = Blueprint('routes', __name__, url_prefix='/')

# create shipping label
@bp.route('/api/delivery/generatelabel/<transact_id>', methods=['POST'])
def create_label(transact_id):    
    transaction = models.Transaction.query.get(transact_id)
    return transaction.shipping_label

# create a delivery
@bp.route('api/delivery/create/<transact_id>',methods=['POST'])
def schedule_delivery(transact_id):
    new_info = request.form
    package_size = new_info['package_size'] # small package or med / large boxes
    courier = new_info['courier'] # DHL, EMS, Fedex
    shipping_option = new_info['shipping_option'] # standard or expedited

    transaction = models.Transaction.query.get(transact_id)
    seller = models.User.query.get(transaction.receiver_id)
    buyer = models.User.query.get(transaction.buyer_id)
    
    Delivery(transact_id, package_size, courier, shipping_option, \
        seller.username, seller.address_1, seller.address_2, seller.address_city, seller.address_state, seller.address_zip,\
            buyer.username, buyer.address_1, buyer.address_2, buyer.address_city, buyer.address_state, buyer.address_zip)
    
    return True
    
# get tracking info of a delivery
@bp.route('/api/delivery/tracking/<delivery_id>', methods=['GET'])
def view_tracking(delivery_id):
    delivery = models.Delivery.query.get(delivery_id)
    return delivery.get_tracking()