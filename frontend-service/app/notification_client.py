from flask import session
import requests

def get_ip():
    auction_service_ip = "notification"
    return auction_service_ip

def get_port():
    return 5000

def get_emails():

    # Tell server to refresh
    url = 'http://{}:{}/api/receive_msg'.format(get_ip(), get_port())
    response = requests.get(url)

    # Get the emails
    url = 'http://{}:{}/api/get_all_msg'.format(get_ip(), get_port())
    response = requests.get(url)

    if response.status_code == 200:
        print(response.json())
        return response.json()


def send_email(message_id, message):

    url = 'http://{}:{}/api/reply_msg/{}'.format(get_ip(), get_port(), message_id)

    data = {'reply_text': message}

    response = requests.post(url, data)

    if response.status_code == 200:
        print(response.json())
        return response.json()