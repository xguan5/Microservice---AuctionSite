from flask import session
import requests


def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip
    
def get_all_auctions():
    url = 'http://{}:5000/api/auctions'.format(get_ip())
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_auction_details(auction_id):
    url = 'http://{}:5000/api/auction/{}'.format(get_ip(), auction_id)
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
