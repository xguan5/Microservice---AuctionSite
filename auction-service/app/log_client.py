from flask import session
import requests


def get_ip():
    #log_service_ip = "localhost"
    log_service_ip = "127.0.0.1"
    return log_service_ip

def get_port():
    return 5006
    
def create_log(data):

    # return {
    #     'result': True,
    #     'content': 'Success'
    # }
    print('data is ',data)
    url = 'http://{}:{}/api/create_log'.format(get_ip(), get_port())

    response = requests.post(url=url, data=data)
    print("posted to mongo")

    if response.status_code == 200:
        print(response.json())
        return response.json()