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
