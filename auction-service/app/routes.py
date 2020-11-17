
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
	return res

#get one auction
@bp.route('/api/auction/<id>',methods = ['GET'])
def get_auction(id):
	auction = models.Auction.query.get(id)
	return jsonify({'result': auction.to_json()})

#create a new auction
@bp.route('api/auction/create',methods=['POST'])
def create_auction():
	#content = request.get_json(force=True)
	content = request.form
	name = content['name']
	buy_now_price = content['buy_now_price']
	start_bid_price = content['start_bid_price']
	inc_bid_price = content['inc_bid_price']
	start_time = content['start_time']
	end_time = content['end_time']
	creator = content['creator']
	item = content['item']

	new_auction = models.Auction(name,buy_now_price,start_bid_price,inc_bid_price,start_time,end_time,creator,item)

	models.db.session.add(new_auction)
	models.db.session.commit()

	return jsonify({'result': new_auction.to_json()})


#update a auction
@bp.route('/api/auction/<id>',methods=['PUT'])
def update_auction(id):
	auction = models.Auction.query.get(id)

	content = request.form
	name = content['name']
	buy_now_price = content['buy_now_price']
	start_bid_price = content['start_bid_price']
	inc_bid_price = content['inc_bid_price']
	start_time = content['start_time']
	end_time = content['end_time']
	creator = content['creator']
	item = content['item']

	auction.name = name
	auction.buy_now_price = buy_now_price
	auction.start_bid_price = start_bid_price
	auction.inc_bid_price = inc_bid_price
	auction.start_time = start_time
	auction.end_time = end_time
	auction.creator = creator
	auction.item = item

	models.db.session.commit()

	return jsonify({'result': auction.to_json()})

#delete auction
@bp.route('/api/auction/<id>',methods=['DELETE'])
def delete_auction(id):
	auction = models.Auction.query.get(id)
	models.db.session.delete(auction)
	models.db.session.commit()
	return jsonify({'result': auction.to_json()})


#get all biddings for a given auction
@bp.route('/api/auction/<id>/bids', methods=['GET'])
def get_bids(id):
	#auction = models.Auction.query.get(id)
	all_biddings = []
	for row in models.Bidding.query.filter_by(auction_id=id):
		all_biddings.append(row.to_json())
	res = jsonify(all_biddings)
	return res

#add bidding to auction
@bp.route('api/auction/<id>/createbid',methods=['POST'])
def create_bid(id):
	content = request.form
	print(content)
	
	bidder = content['user_id']
	bid_price = content['bid_price']
	bid_placed = content['bid_placed']

	new_bid = models.Bidding(bidder,id,bid_price,bid_placed)

	models.db.session.add(new_bid)
	models.db.session.commit()

	return jsonify({'result': new_bid.to_json()})

#no need for update bid and delete bid, since we won't allow user to do that

