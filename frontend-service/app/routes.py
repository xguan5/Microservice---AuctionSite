
import os
import sys
import datetime
import traceback
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, escape, json, jsonify, Response, Blueprint
import requests
from . import user_client as users
from . import auction_client as auctions
from . import authentication_client as auth
from . import item_client as items
from . import notification_client as notifications
from . import payment_client as payments
from . import delivery_client as delivery

import psycopg2

bp = Blueprint('routes', __name__, url_prefix='/')


def check_login():
    if not session.get('username'): return False
    return auth.check_login(session.get('username'))

#*********************************************************************
# Home, display list of auctions
#*********************************************************************
@bp.route('/', methods=['GET'])
@bp.route('/auction_list', methods=['GET'])
@bp.route('/auction_list/<sort>', methods=['GET', 'POST'])
def auction_list(sort='start_time'):
    error=None

    if not check_login():
        return redirect( url_for('routes.login') )

    auction_list = auctions.get_all_auctions()
    
    categories = items.get_all_categories()
    for auction in auction_list:
        auction['item'] = items.get_item_details(auction['item'])['result']
        auction['current_bid'] = auctions.get_highest_bid(auction['id'])['max_bid']
        for category in categories:
            if category['id'] == auction['item']['category']:
                auction['item']['category_details'] = category
                break
            auction['item']['category_details'] = {
                'id': None,
                'name': None
            }

    if request.form.get('search_term'):
        search_term = request.form.get('search_term')
    else:
        search_term = False


    auction_list = sorted(auction_list, key = lambda i: i[sort])

    return_list = []
    for auction in auction_list:
        if search_term:
            if auction['item']['category_details']['name'] and search_term.lower() in auction['item']['category_details']['name'].lower():
                return_list.append(auction)
            elif auction['item']['name'] and search_term.lower() in auction['item']['name'].lower():
                return_list.append(auction)
            elif auction['item']['description'] and search_term.lower() in auction['item']['description'].lower():
                return_list.append(auction)
            elif auction['name'] and search_term.lower() in auction['name'].lower():
                return_list.append(auction)
        else:
            return_list.append(auction)

    return_list = list(filter(lambda d: d['status'].replace(' ', '') == 'Active', return_list))


    template = render_template('auction_list.html', 
        auction_list=return_list,
        sort=sort
    )
    
    return template

@bp.route('/auction/create', methods=['GET', 'POST'])
def create_auction():
    error = None
    auction=None
    item=None

    print(request.form)

    categories = items.get_all_categories()

    if request.method == 'POST':
        try:
            start_datetime = datetime.datetime.combine(datetime.datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'), datetime.datetime.strptime(request.form.get('start_time'), '%H:%M').time()) 
            end_datetime = start_datetime + datetime.timedelta(hours=int(request.form['duration']))
        except Exception as e:
            return render_template('create_auction.html', auction=auction, item=item, categories=categories, error='Invalid Start Time: %s' % str(e))

        if request.form['new_category'] and request.form['new_category'] != '':
            category_response = items.create_category(request.form['new_category'])
            category = category_response['result']['id']
        else:
            category = request.form['category']
            
        item_data = {
            'name': request.form['item_name'],
            'description': request.form['item_description'],
            'name': request.form['item_name'],
            'category': category
        }

        item_result = items.create_item(item_data)

        if not request.form.get('image_url') or request.form.get('image_url') == '':
            image_url = 'https://lh3.googleusercontent.com/proxy/3SeeYKkyo-5HciaBCdqZrPukroxnUNAzTRgEjo5JDV-jnGHD8SDrDX8X6Uow0W1M5WgqdtrSja0bKhg83MJbBTNIpKNDJ5Bi9irj2uVNGt3JxSny'
        else:
            image_url = request.form.get('image_url')

        auction_data = {
            'name': request.form['auction_name'],
            'buy_now_price': request.form['buy_now_price'],
            'start_bid_price': request.form['start_bid_price'],
            'inc_bid_price': request.form['inc_bid_price'],
            'start_time': start_datetime,
            'end_time': end_datetime,
            'creator': session.get('username'),
            'item': item_result['result']['id'],
            'image_url': image_url
        }

        auction_result = auctions.create_auction(auction_data)

        if auction_result.get('result'):
            return get_auction_details(auction_id=auction_result['content']['id'])
        else:
            error = auction_result.get('content')

    template = render_template('create_auction.html', auction=auction, item=item, categories=categories, error=error)

    return template

@bp.route('/auction/update/<auction_id>', methods=['GET', 'POST'])
def update_auction(auction_id):

    auctions.update_auction(auction_id, data=request.form)

    return redirect(url_for('routes.get_auction_details', auction_id=auction_id))

@bp.route('/auction/bid/<auction_id>', methods=['GET', 'POST'])
def place_bid(auction_id, message=None):
    
    try:
        amount = int(request.form.get('bid_amount'))
    except Exception as e:
        return get_auction_details(auction_id=auction_id, bid_error="Invalid Bid Format")

    response = auctions.place_bid(auction_id, session.get('username'), amount, datetime.datetime.now())

    print(response)

    if response['result'] == False:
        bid_error = response['content']
    else:
        bid_error = None
        message = "Bid Placed!"

    return get_auction_details(auction_id=auction_id, bid_error=bid_error, message=message)

@bp.route('/auction/buy-now/<auction_id>', methods=['GET', 'POST'])
def buy_now(auction_id):

    print('Hello %s' % request.form)

    amount = request.form.get('buy_now_price_bid')
    try:
        amount = amount.split('.')[0]
    except Exception as e:
        pass

    amount = int(amount)

    users.add_to_cart(session.get('username'), auction_id)
    auctions.update_auction(auction_id, data={'status': 'end'})
    auctions.place_bid(auction_id, session.get('username'), amount, datetime.datetime.now())

    return get_auction_details(auction_id=auction_id, bid_error=None, message="Item Added to Cart!")

@bp.route('/auction/end-auction/<auction_id>', methods=['GET', 'POST'])
def end_auction(auction_id):

    data = {
        'status': 'end',
        'end_time': datetime.datetime.now()
    }

    auctions.update_auction(auction_id, data)

    return get_auction_details(auction_id=auction_id)

@bp.route('/auction/add-to-watchlist', methods=['GET', 'POST'])
def add_to_watchlist():

    response = users.add_to_watchlist(session.get('username'), request.form)

    return user_details(username=session.get('username'))

@bp.route('/auction/flag-item/<item_id>/<auction_id>', methods=['GET', 'POST'])
def flag_item(item_id, auction_id):

    response = items.flag_item(item_id)

    print(response)

    return get_auction_details(auction_id=auction_id)

@bp.route('/cart', methods=['GET', 'POST'])
def get_cart():

    response = users.get_cart(session.get('username'))

    cart_list = []

    total = 0

    for item in response['content']:
        auction = auctions.get_auction_details(item['auc_id'])['result']
        auction['price'] = auctions.get_highest_bid(auction['id'])['max_bid']
        cart_list.append(auction) 
        total += auction['price']

    template = render_template('cart.html', cart_list=cart_list, total=total)

    return template

@bp.route('/checkout/<total>', methods=['GET', 'POST'])
def checkout(total):
    
    template = render_template('checkout.html', action='buy', total_amount=total)

    return template

@bp.route('/purchase', methods=['GET', 'POST'])
def purchase():

    try:
        users.clear_cart(session.get('username'))
    except Exception as e:
        print(str(e))
        pass
    try:
        payments.create_payment_method(session.get('username'), data=request.form)
    except Exception as e:
        print(str(e))
        pass
    try:
        delivery.create_shipment(auction_id)
    except Exception as e:
        print(str(e))
        pass

    template = render_template('checkout.html', action='done')

    return template

@bp.route('/auction/<auction_id>', methods=['GET'])
def get_auction_details(auction_id, bid_error=None, message=None):

    auction_details = auctions.get_auction_details(auction_id)
    item_details = items.get_item_details(auction_details['result']['item'])
    categories = items.get_all_categories()

    for category in categories:
        if category['id'] == item_details['result']['category']:
            item_details['result']['category_details'] = category
            break
        item_details['result']['category_details'] = {
            'id': None,
            'name': None
        }
    highest_bid = auctions.get_highest_bid(auction_id)

    try:
        next_bid = max( int(highest_bid['max_bid']) + int(auction_details['result']['inc_bid_price']), int(auction_details['result']['start_bid_price']) + int(auction_details['result']['inc_bid_price']))
    except Exception as e:
        print(e)
        next_bid = 0

    template = render_template('auction_details.html', 
        auction=auction_details.get('result'),
        item=item_details.get('result'),
        categories=categories,
        highest_bid=highest_bid['max_bid'],
        bid_error=bid_error,
        next_bid=next_bid,
        start_bid = auction_details['result']['start_bid_price'],
        message=message
    )
    
    return template

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error=None

    if request.method == 'POST':
        result = auth.login(request.form['username'], request.form['password'])
        if result.get('result') == True:
            session['username'] = request.form['username']
            session['is_admin'] = result['content']
            return redirect(url_for('routes.auction_list'))
        else:
            error = result.get('content')

    template = render_template('login.html', error=error)

    return template

@bp.route('/logout',methods=['POST', 'GET'])
def logout():

     auth.logout(session.get('username'))

     session['username'] = None

     return redirect(url_for('routes.login'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None

    if request.method == 'POST':
        if request.form['is_admin'] == "TRUE": is_admin = True
        else: is_admin = False


        user_result = users.create_user(request.form)
        credential_result = auth.create_credentials(request.form['username'], request.form['password'], is_admin)
        if user_result.get('result') and credential_result.get('result') == True:
            result = auth.login(request.form['username'], request.form['password'])
            session['username'] = request.form['username']
            session['is_admin'] = is_admin
            return redirect(url_for('routes.auction_list'))
        else:
            if user_result.get('result')  == False:
                error = user_result.get('content')
            if credential_result.get('result')  == False:
                error = credential_result.get('content')

    template = render_template('signup.html', error=error)

    return template


@bp.route('/user-updates/<username>',methods=['POST', 'GET'])
def user_update(username):

    users.update_user(username, request.form)

    return user_details(username=username)
    
@bp.route('/user/<username>',methods=['POST', 'GET'])
def user_details(username):

    if username != session.get('username') and not session.get('is_admin'):
        return "<h1>You are not this user and you are not an admin</h1>"

    user_details = users.get_user_details(username)

    #return user_details

    all_bids = auctions.get_all_bids(username=session.get('username'))
    auction_list1 = []
    for bid in all_bids['content']:
        if bid['auction'] not in auction_list1:
            auction_list1.append(bid['auction'])

    auction_list2 = []
    for auction in auction_list1:
        auction_list2.append(auctions.get_auction_details(auction)['result'])

    template = render_template('user_details.html', 
        user_details=user_details.get('content'),
        auction_list=auction_list2
    )
    
    return template


@bp.route('/admin', methods=['GET', 'POST'])
def admin():

    flags = items.get_all_flags()
    categories = items.get_all_categories()
    print(flags)

    auctions_ended_yesterday = 0
    auctions_ended_week = 0
    auctions_ended_month = 0
    auctions_ended_all_time = 0
    all_auctions = auctions.get_all_auctions()
    for auction in all_auctions:
        end_time = auction['end_time']
        if end_time: 
            auctions_ended_all_time += 1
        else: 
            continue
        today = datetime.datetime.now()
        print(end_time)
        end_time = datetime.datetime.strptime(end_time.replace(' GMT', ''), '%a, %d %b %Y %H:%M:%S')
        print(end_time)
        if end_time == today - datetime.timedelta(days=1):
            auctions_ended_yesterday += 1
        elif end_time >= today - datetime.timedelta(days=7):
            auctions_ended_week += 1
        elif end_time >= today - datetime.timedelta(days=31):
            auctions_ended_month += 1

    for flag in flags:
        flag['item'] = items.get_item_details(flag['items'])['result']
    template = render_template('admin.html', categories=categories, flags=flags, auctions_ended_yesterday=auctions_ended_yesterday, auctions_ended_week=auctions_ended_week, auctions_ended_month=auctions_ended_month,  auctions_ended_all_time=auctions_ended_all_time)

    return template

@bp.route('/emails', methods=['GET', 'POST'])
def emails(status=None):

    emails = notifications.get_emails()

    blocked_senders = ['googlecommunityteam-noreply@google.com', 'no-reply@accounts.google.com']
    emails_return_2 = list(filter(lambda d: d['sender'] not in blocked_senders, emails))

    template = render_template('emails.html', emails=emails_return_2, status=status)

    return template

@bp.route('/email_response/<message_id>', methods=['GET', 'POST'])
def email_response(message_id):

    print(request.form)

    message = request.form.get('message_text')

    notifications.send_email(message_id, message)

    return emails(status="Message Sent!")

@bp.route('/admin/category-update', methods=['GET', 'POST'])
def category_update():

    print(request.form)

    for key in request.form:
        if key == 'new_category':
            if request.form[key] and request.form[key] != "":
                items.create_category(request.form[key])
        else: 
            items.update_category(key, request.form[key])

    return admin()