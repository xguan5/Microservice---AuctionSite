from flask import session
import requests

def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip

def get_port():
    return 5001
""" 
payment: 5003
item: 5004
delivery: 5006
notification: 5007
"""

def create_user(data):

    url = 'http://{}:{}}/api/create_account'.format(get_ip(), get_port())

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