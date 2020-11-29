from flask import session
import requests


def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip

def get_port():
    return 5005
    
def get_all_auctions():
    url = 'http://{}:{}/api/auctions'.format(get_ip(), get_port())
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_auction_details(auction_id):
    url = 'http://{}:{}/api/auction/{}'.format(get_ip(), get_port(), auction_id)
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def create_auction(data):

    url = 'http://{}:{}/api/auction/create'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_highest_bid(id):
    url = 'http://{}:{}/api/auction/{}/highestbid'.format(get_ip(), get_port(), id)

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def place_bid(id, user_id, amount, placed_time):
    url = 'http://{}:{}/api/auction/{}/createbid'.format(get_ip(), get_port(), id)

    data = {
        'user_id': user_id,
        'bid_price': amount,
        'bid_placed': placed_time
    }

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def update_auction(auction_id, data):
    url = 'http://{}:{}/api/auction/{}'.format(get_ip(), get_port(), auction_id)

    response = requests.put(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()
