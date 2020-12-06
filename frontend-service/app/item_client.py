from flask import session
import requests

def get_ip():
    auction_service_ip = "item"
    return auction_service_ip

def get_port():
    return 5000
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

def create_item(data):

    url = 'http://{}:{}/api/item/create'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def get_all_flags():

    url = 'http://{}:{}/api/flags'.format(get_ip(), get_port())

    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def flag_item(item_id):

    url = 'http://{}:{}/api/flag/create'.format(get_ip(), get_port())

    data = {'name': 'Flagged by User', 'item_id': item_id}

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()