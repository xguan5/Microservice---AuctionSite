from flask import session
import requests

def get_ip():
    auction_service_ip = "delivery"
    return auction_service_ip

def get_port():
    return 5000
""" 
notification: 5007
"""

def create_shipment(auction_id):

    url = 'http://{}:{}/api/delivery/create/{}'.format(get_ip(), get_port(), auction_id)

    data = {'package_size': 'medium', 'courier': 'DHL', 'shipping_option': 'standard'}

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

