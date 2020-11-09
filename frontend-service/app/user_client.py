from flask import session
import requests


def get_user_list():

    url = 'http://0.0.0.0:5090/api/user_list'
    #url = 'http://localhost:5001/api/user_list'
    response = requests.get(url=url)

    if response.status_code == 200:
        print(response.json())
        return response.json()
