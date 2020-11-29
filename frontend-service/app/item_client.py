from flask import session
import requests

def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip

def get_port():
    return 5004
""" 
delivery: 5006
notification: 5007
"""

def get_all_categories():

    url = 'http://{}:{}/api/categories'.format(get_ip(), get_port())

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def update_category(id, name):

    url = 'http://{}:{}/api/category/{}'.format(get_ip(), get_port(),id)

    data = {'name': name}

    print(url, data)

    response = requests.put(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def create_category(name):

    url = 'http://{}:{}/api/category/create'.format(get_ip(), get_port())

    data = {'name': name}

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()


def get_item_details(id):
    url = 'http://{}:{}/api/item/{}'.format(get_ip(), get_port(), id)

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()