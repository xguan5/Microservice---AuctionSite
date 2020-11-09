from flask import session
import requests


def get_user_list():

    user_service_ip = "172.20.0.1"
    url = 'http://{}:5090/api/user_list'.format(user_service_ip)
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
