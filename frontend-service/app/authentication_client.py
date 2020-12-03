from flask import session
import requests


def get_ip():
    auction_service_ip = "authentication-service_api_1"
    return auction_service_ip

def get_port():
    return 5000
    
def login(username, password):
    url = 'http://{}:{}/api/authentication/login'.format(get_ip(), get_port())

    body = {'username': username, 'password': password}
    response = requests.post(url=url, data=body)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def logout(username):
    url = 'http://{}:{}/api/authentication/logout'.format(get_ip(), get_port())

    body = {'username': username}
    response = requests.post(url=url, data=body)

    if response.status_code == 200:
        print(response.json())
        return response.json()

def create_credentials(username, password, is_admin):
    url = 'http://{}:{}/api/authentication/create'.format(get_ip(), get_port())

    body = {'username': username, 'password': password, 'is_admin': is_admin}
    response = requests.post(url=url, data=body)

    if response.status_code == 200:
        print(response.json())
        return response.json()

    else:
        print('here')

def check_login(username):
    url = 'http://{}:{}/api/authentication/check'.format(get_ip(), get_port())

    body = {'username': username}
    response = requests.post(url=url, data=body)

    if response.status_code == 200 and response.json()['result']:
        return True
    else:
        return False