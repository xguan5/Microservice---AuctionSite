from flask import session
import requests

def get_ip():
    auction_service_ip = "user"
    return auction_service_ip

def get_port():
    return 5000

def create_user(data):

    url = 'http://{}:{}/api/create_account'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print('ResponseChip, ', response.json())
        return response.json()

def update_user(username, data):
    url = 'http://{}:{}/api/update_profile'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_user_details(username):
    url = 'http://{}:{}/api/view_profile/{}'.format(get_ip(), get_port(), username)

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def add_to_watchlist(username, auction_id):

    url = 'http://{}:{}/add_to_watchlist/{}&{}'.format(get_ip(), get_port(), username, auction_id)

    response = requests.get(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()