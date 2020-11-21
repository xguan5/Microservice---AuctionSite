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
