from flask import Flask, make_response, abort, request, session, g, redirect, \
    redirect, url_for, abort, render_template, flash, escape, json, jsonify,\
        Response, Blueprint
from . import models
from datetime import datetime
import os
import sys
import traceback
import time
import random

bp = Blueprint('routes', __name__, url_prefix='/')

# get payment methods for a user
@bp.route('/api/PaymentMethod/<id>', methods=['GET'])
def get_PaymentMethod(id):
	pmt_methods = []
	for row in models.PaymentMethod.query.all():
		if userid == row.user_id:
			pmt_methods.append(row.to_json())
	pmt_methods_dict = jsonify(pmt_methods)
	return pmt_methods_dict

# create a payment method
@bp.route('api/create_paymentmethod/<u_id>',methods=['GET','POST'])
def create_PaymentMethod(u_id):
	new_info = request.form
	
	card_num = new_info['card_num']
	billing_name = new_info['billing_name']
	billing_address1 = new_info['billing_address1']
	billing_address2 = new_info['billing_address2']
	billing_city = new_info['billing_city']
	billing_zip = new_info['billing_zip']
	billing_state = new_info['billing_state']
	billing_country = new_info['billing_country']
	exp_date = new_info['exp_date']
	csv_code = new_info['csv_code']

	new_PaymentMethod = PaymentMethod(u_id, card_num, billing_name, \
        billing_address1, billing_address2, billing_city, billing_zip, \
            billing_state, billing_country, exp_date, csv_code)

	db.session.add(new_PaymentMethod)
	db.session.commit()

	return jsonify({'result': True, 'content',new_PaymentMethod.to_json()})


# update a payment method
@bp.route('/api/PaymentMethod/<pmtid>',methods=['PUT'])
def update_PaymentMethod(pmtid):
	pmt_method = models.PaymentMethod.query.get(pmtid)

	new_info = request.form
	billing_name = new_info['billing_name']
	billing_address1 = new_info['billing_address1']
	billing_address2 = new_info['billing_address2']
	billing_city = new_info['billing_city']
	billing_zip = new_info['billing_zip']
	billing_state = new_info['billing_state']
	billing_country = new_info['billing_country']
	exp_date = new_info['exp_date']
	csv_code = new_info['csv_code']

	pmt_method.billing_name = billing_name
	pmt_method.billing_address1 = billing_address1
	pmt_method.billing_address2 = billing_address2
	pmt_method.billing_city = billing_city
	pmt_method.billing_zip = billing_zip
	pmt_method.billing_state = billing_state
	pmt_method.billing_country = billing_country
	pmt_method.exp_date = exp_date
	pmt_method.csv_code = csv_code

	models.db.session.commit()

	return jsonify({'result': pmt_method.to_json()})

# delete a payment method
@bp.route('/api/PaymentMethod/<pmtid>',methods=['DELETE'])
def delete_PaymentMethod(pmtid):
	pmt_method = models.PaymentMethod.query.get(pmtid)
	models.db.session.delete(pmt_method)
	models.db.session.commit()
	return jsonify({'result': pmt_method.to_json()})

@bp.route('api/viewcart/<userid>/checkout',methods = ['POST'])
def check_out_cart(userid):
	cart = jason.loads(view_cart(userid))
	check_out_count = 0

	for auc in cart:
		if auc[status] == 'end' and auc[winner_id] == userid:
			temp = models.Transaction(userid, auc[creator],auc.bid_price, "T" & str(random.rand()*1000000), ), 
			process_transaction(temp)
			check_out_count += 1
	
	clear_cart(userid)

	if check_out_count > 0:
		return True # checked out something
	else:
		return False # nothing to checkout
