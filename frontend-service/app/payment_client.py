from flask import session
import requests

def get_ip():
    auction_service_ip = "payment"
    return auction_service_ip

def get_port():
    return 5000


def create_payment_method(username, data):

    url = 'http://{}:{}/api/PaymentMethod/create/{}'.format(get_ip(), get_port(), username)

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()
