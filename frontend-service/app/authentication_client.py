from flask import session
import requests


def get_ip():
    auction_service_ip = "localhost"
    return auction_service_ip
    
def login(user_id, password):
    url = 'http://{}:5001/api/authentication/login'.format(get_ip())

    body = {'user_id': user_id, 'password': password}
    response = requests.post(url=url, data=body)

    if response.status_code == 200:
        print(response.json())
        return response.json()

