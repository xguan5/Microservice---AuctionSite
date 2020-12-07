
import os
import sys
from datetime import datetime, timedelta
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import models as models
from . import log_client as logs
import pika
from sqlalchemy import and_
#from pandas.io.json import json_normalize

bp = Blueprint('routes', __name__, url_prefix='/')

#set up rabbitmq, pubsub
@bp.route('/add-job', methods=['POST'])
def add_log(msg):
	try:
		credentials = pika.PlainCredentials(username='guest', password='guest')
		connection = pika.BlockingConnection(pika.ConnectionParameters(host='messaging',port=5672,credentials=credentials))
		channel = connection.channel()
		channel.exchange_declare(exchange='logs', exchange_type='fanout')
		channel.basic_publish(exchange='logs', routing_key='', body=msg)
		#channel.queue_declare(queue='hello')
		#channel.basic_publish(exchange='', routing_key='hello', body=msg)
		print(connection)
		print(msg)
		connection.close()
		return " [x] Sent %s" % msg
	except Exception as e:
		print(str(e))
		return "Pass"


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
	image_url = content['image_url']

	new_auction = models.Auction(name,buy_now_price,start_bid_price,inc_bid_price,start_time,end_time,creator,item, image_url)
	log_result = json.dumps({'service':'auction','action':'create auction','timestamp':datetime.now(),'content':json.dumps(content)})

	add_log(log_result)

	models.db.session.add(new_auction)
	models.db.session.commit()

	note_msg_creator = json.dumps({'msg_type':'notification','timestamp':datetime.now(),'content':'new_auction successfully created','receiver':creator,'content':str(new_auction.id)})
	add_log(note_msg_creator)

	# schedule start and stop, as well as alerts
	url = 'http://notification:5000/api/schedule_alerts'

	data = {
		'auc_id': new_auction.id,
		'end_time': new_auction.end_time,
		'start_time': new_auction.start_time
	}

	r = requests.post(url, data=data)

	# notify watchlist matches, if there are any
	url = 'http://user:5000/api/check_match/'

	data = {
		'auc_id': new_auction.id,
		'buy_now_price': buy_now_price,
		'start_bid_price': start_bid_price,
		'name': name
	}

	r = requests.post(url, data=data)

	return jsonify({'result': True, 'content': new_auction.to_json()})


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

	log_result = json.dumps({'msg_type':'log','service':'auction','action':'update auction','timestamp':datetime.now(),'content':json.dumps(content)})
	add_log(log_result)
	models.db.session.commit()

	return jsonify({'result': auction.to_json()})

#delete auction
@bp.route('/api/auction/<id>',methods=['DELETE'])
def delete_auction(id):
	auction = models.Auction.query.get(id)
	models.db.session.delete(auction)
	models.db.session.commit()
	log_result = json.dumps({'msg_type':'log','service':'auction','action':'delete auction','timestamp':datetime.now(),'content':'deleted auction {}'.format(id)})
	add_log(log_result)
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

	print(bid_price, ' ', incremental_bid, ' ', cur_high_bid)
	print(int(bid_price) - int(cur_high_bid))
	print(int(incremental_bid))
	print(int(bid_price) - int(cur_high_bid) < int(incremental_bid))
	print(int(bid_price) - int(starting_bid))
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
	elif int(bid_price) - int(cur_high_bid) < int(incremental_bid) :
		success = False
		return {'result':success,'content':'new bid must be higher than existing bids at least by the incremental amount'}
	elif int(bid_price) - int(starting_bid) < int(incremental_bid):
		success = False
		return {'result':success,'content':'new bid must be higher than starting bid at least by the incremental amount'}
	else:
		try:
			prev_high_bidder = models.Bidding.query.filter_by(bid_price = cur_high_bid).first().to_json()['user']
		except Exception as e:
			prev_high_bidder = None
		auction = models.Auction.query.get(id)
		seller = auction.creator_id

		new_bid = models.Bidding(bidder,id,bid_price,bid_placed)

		models.db.session.add(new_bid)
		models.db.session.commit()

		success = True
		log_result = json.dumps({'msg_type':'log','service':'auction','action':'create bid','timestamp':datetime.now(),'content':json.dumps(content)})
		add_log(log_result)
		#new bid placed, notify the previous highest bidder

		note_msg_prevhigh = json.dumps({'msg_type':'notification','timestamp':datetime.now(),'content':'higher bid placed, notify the previous high bidder','receiver':prev_high_bidder})
		add_log(note_msg_prevhigh)


		if prev_high_bidder:
			note_msg_prevhigh = json.dumps({'timestamp':datetime.now(),'content':'higher bid placed, notify the previous high bidder','receiver':prev_high_bidder})
			add_log(note_msg_prevhigh)

			user_url = 'http://user:5000/api/view_profile/' + str(prev_high_bidder)
			response = requests.get(user_url)
			recipient = response["content"]["email"]

			url = 'http://notification:5000/api/send_auto_msg'

			data = {
				'msg': 'outbid',
				'parameters': [auction["item"], new_bid.auction_id, new_bid.bid_price],
				'user_email': recipient
			}

			r = requests.post(url, data=data)


		#new bid placed, notify the seller
		note_msg_seller = json.dumps({'msg_type':'notification','timestamp':datetime.now(),'content':'new bid placed, notify the seller','receiver':seller})
		add_log(note_msg_seller)

		user_url = 'http://user:5000/api/view_profile/' + str(seller)
		response = requests.get(user_url)
		recipient = response["content"]["email"]

		url = 'http://notification:5000/api/send_auto_msg'

		data = {
			'msg': 'new bid',
			'parameters': [auction["item"], new_bid.auction_id, new_bid.bid_price],
			'user_email': recipient
		}

		r = requests.post(url, data=data)

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

#return metric of auctions within some time interval, rabbitmq msg to notification

#return the highest bid so far
@bp.route('/api/auction/all-bids/<username>', methods=['GET'])
def all_bids(username):
	all_bids = []
	for row in models.Bidding.query.filter_by(user_id=username):
		all_bids.append(row.to_json())

	return json.dumps({'content': all_bids})


#return all active auctions

#if an auction ends in predetermined timeframe, msg notification service
#search auction by end time, it should be passed in as {‘day':1,'hour':1}
@bp.route('/api/auction/findopen/<day>/<hour>',methods =['GET'])
def find_auction_open(day,hour):

	time_left = timedelta(days=int(day),hours=int(hour))
	time_over = time_left + datetime.now()
	results = []
	for row in models.Auction.query.filter(and_(models.Auction.end_time <= time_over,models.Auction.end_time > datetime.now() )):
		results.append(row.to_json())
	res = jsonify(results)

	receipients = ''
	for row in results:
		receipients += str(row['creator']) + ', '

	note_msg_auctions = json.dumps({'msg_type':'notification','timestamp':datetime.now(),'content':'auction close in {} day, {} hour, notify relevant users'.format(day, hour),'receiver':receipients})
	add_log(note_msg_auctions)

	return res

@bp.route('/api/auction/findclosed/<day>/<hour>',methods =['GET'])
def find_auction_close(day,hour):

	time_gap = timedelta(days=int(day),hours=int(hour))
	time_over = datetime.now() - time_gap
	results = []
	for row in models.Auction.query.filter(and_(models.Auction.end_time == time_over,models.Auction.end_time < datetime.now() )):
		results.append(row.to_json())
	res = jsonify(results)

	return res







