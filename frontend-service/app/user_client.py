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

    return {
        'result': True,
        'content': 'Success'
    }

    url = 'http://{}:{}/api/create_account'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def update_user(username, data):
    return {
        'result': True,
        'content': 'Success'
    }

    url = 'http://{}:{}/api/create_account'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_user_details(username):

    return { 
        'result': True,
        'content': {
            'username': 'clocke',
            'email': 'Chip@test.com',
            'address_1': '123 fake st',
            'address_2': 'Apt 2',
            'address_city': 'Rochester',
            'address_state': 'MN',
            'address_zip': '55902',
            'status': 'Active'
        }
    }

    url = 'http://{}:{}/api/view_profile/{}'.format(get_ip(), get_port(), username)

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()