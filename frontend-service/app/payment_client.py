from flask import session
import requests

def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip

def get_port():
    return 5003


def create_user(data):

    url = 'http://{}:{}/api/create_account'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)

    if response.status_code == 200:
        print(response.json())
        return response.json()
