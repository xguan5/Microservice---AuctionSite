
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import models as models

bp = Blueprint('routes', __name__, url_prefix='/')

#get all auctions
@bp.route('/api/auctions', methods=['GET'])
def get_auctions():
	all_auctions = []
	for row in models.Auction.query.all():
		all_auctions.append(row.to_json())
	res = jsonify(all_auctions)
	print(res)
	return res

#get one auction
@bp.route('/api/auction/<id>',methods = ['GET'])
def get_auction(id):
	auction = models.Auction.query.get(id)
	return jsonify({'result': auction.to_json()})

#create a new auction
@bp.route('api/auction/create',methods=['POST'])
def create_auction():
	content = request.get_json(force=True)
	
	name = content['name']

	new_auction = models.Auction(name)

	models.db.session.add(new_auction)
	models.db.session.commit()

	return jsonify({'result': new_auction.to_json()})


#update a auction
@bp.route('/api/auction/<id>',methods=['PUT'])
def update_auction(id):
	auction = models.Auction.query.get(id)

	content = request.get_json()
	name = content['name']

	auction.name = name

	models.db.session.commit()

	return jsonify({'result': auction.to_json()})

#delete auction
@bp.route('/api/auction/<id>',methods=['DELETE'])
def delete_product(id):
	auction = models.Auction.query.get(id)
	models.db.session.delete(auction)
	models.db.session.commit()
	return jsonify({'result': auction.to_json()})


