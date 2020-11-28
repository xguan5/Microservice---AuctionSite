
import os
import sys
from datetime import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import models as models
from . import log_client as logs
#from pandas.io.json import json_normalize 

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
#To do: trigger notification
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
	log_result = json.dumps(logs.create_log({'service':'auction','action':'create auction','timestamp':datetime.now(),'content':json.dumps(content)}))

	models.db.session.add(new_auction)
	models.db.session.commit()

	return jsonify({'result': new_auction.to_json()})


#update a auction, use this to mark end and start of auction by setting status
@bp.route('/api/auction/<id>',methods=['PUT'])
def update_auction(id):
	auction = models.Auction.query.get(id)

	content = request.form
	if 'name' in content.keys():
		name = content['name']
		auction.name = name
	if 'buy_now_price' in content.keys():
		buy_now_price = content['buy_now_price']
		auction.buy_now_price = buy_now_price
	if 'start_bid_price' in content.keys():
		start_bid_price = content['start_bid_price']
		auction.start_bid_price = start_bid_price
	if 'inc_bid_price' in content.keys():
		inc_bid_price = content['inc_bid_price']
		auction.inc_bid_price = inc_bid_price
	if 'start_time' in content.keys():
		start_time = content['start_time']
		auction.start_time = start_time
	if 'end_time' in content.keys():
		end_time = content['end_time']
		auction.end_time = end_time
	if 'creator' in content.keys():
		creator = content['creator']
		auction.creator = creator
	if 'item' in content.keys():
		item = content['item']
		auction.item = item
	if 'status' in content.keys():
		status = content['status']
		auction.status = status

	log_result = json.dumps(logs.create_log({'service':'auction','action':'update auction','timestamp':datetime.now(),'content':json.dumps(content)}))
	models.db.session.commit()

	return jsonify({'result': auction.to_json()})

#delete auction
@bp.route('/api/auction/<id>',methods=['DELETE'])
def delete_auction(id):
	auction = models.Auction.query.get(id)
	models.db.session.delete(auction)
	models.db.session.commit()
	log_result = json.dumps(logs.create_log({'service':'auction','action':'delete auction','timestamp':datetime.now(),'content':'deleted auction {}'.format(id)}))

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

#return the highest bid so far
@bp.route('/api/auction/<id>/highestbid', methods=['GET'])
def highest_bid(id):
	all_bids = json.loads(get_bids(id).data.decode('utf-8').replace("'", '"'))
	#all_bids = json.dumps(raw_bids, indent=4, sort_keys=True)
	max_bid = 0
	for it in all_bids:
		if it['bid_price'] > max_bid:
			max_bid = it['bid_price']
	return jsonify({'max_bid':max_bid})

#return the start bid price of an auction
@bp.route('/api/auction/<id>/startbid',methods = ['GET'])
def start_bid(id):
	auction = models.Auction.query.get(id)
	res = jsonify(auction.start_bid_price)
	return res

#return the incremental bid price of an auction
@bp.route('/api/auction/<id>/incbid',methods = ['GET'])
def inc_bid(id):
	auction = models.Auction.query.get(id)
	res = jsonify(auction.inc_bid_price)
	return res

#add bidding to auction
@bp.route('api/auction/<id>/createbid',methods=['POST'])
def create_bid(id):
	content = request.form
	
	bidder = content['user_id']
	bid_price = content['bid_price']
	bid_placed = content['bid_placed']

	#check new bid is higher than existing
	#to do: check if higher than starting bid,higher by inc_bid
	cur_high_bid = json.loads(highest_bid(id).data.decode('utf-8').replace("'", '"'))['max_bid']
	starting_bid = json.loads(start_bid(id).data.decode('utf-8').replace("'", '"'))
	incremental_bid = json.loads(inc_bid(id).data.decode('utf-8').replace("'", '"'))
	
	auction = models.Auction.query.get(id)
	if auction.end_time < datetime.now() or auction.status == 'end':
		success = False
		return {'result':success,'content':'Auction is already over, cannot place new bid'}
	if int(bid_price) < int(cur_high_bid):
		#raise value error or jsonify in 'status: error'
		success = False
		return {'result':success,'content':'new bid must be higher than existing bids'}
	elif int(bid_price) < int(starting_bid):
		success = False
		return {'result':success,'content':'new bid must be higher than starting bid price'}
	elif int(bid_price) - int(cur_high_bid) < int(incremental_bid) or int(bid_price) - int(starting_bid) < int(incremental_bid):
		success = False
		return {'result':success,'content':'new bid must be higher than existing bids at least by the incremental amount'}	
	else:
		new_bid = models.Bidding(bidder,id,bid_price,bid_placed)

		models.db.session.add(new_bid)
		models.db.session.commit()

		success = True
		log_result = json.dumps(logs.create_log({'service':'auction','action':'create bid','timestamp':datetime.now(),'content':json.dumps(content)}))

		return jsonify({'result': success, ' content': new_bid.to_json()})

#no need for update bid and delete bid, since we won't allow user to do that

#check if auction status
@bp.route('/api/auction/<id>/status',methods = ['GET'])
def get_status(id):
	auction = models.Auction.query.get(id)
	res = jsonify(auction.status)
	return res



#find winner of an auction
#front end udpate auction with winner
@bp.route('/api/auction/<id>/winner',methods = ['GET'])
def find_auction_winner(id):
	#need to check if auction is over
	auction = models.Auction.query.get(id)
	if datetime.now() > auction.end_time or auction.status != 'end':
		high_bid = json.loads(highest_bid(id).data.decode('utf-8').replace("'", '"'))['max_bid']
		win_bid = models.Bidding.query.filter_by(bid_price = high_bid).first()
		win_bidder = win_bid.to_json()['user']
		success = True
		return jsonify({'result': success, 'content': win_bidder})
	else:
		success = False
		return jsonify({'result': success, 'content': "Auction is not over yet"})


#get winner of an auction
@bp.route('/api/auction/<id>/winner',methods = ['GET'])
def get_auction_winner(id):
	#need to check if auction is over
	auction = models.Auction.query.get(id)
	return jsonify({'result': auction.winner})


