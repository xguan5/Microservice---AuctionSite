from flask import session
import requests


def get_user_list():

    return [
        {
            'username': 'Tester',
            'description': 'Filler Texfeaft',
             'rating': 4.0
        },
        {
            'username': 'Again',
            'description': 'The ith tije acfioj aoi',
             'rating': 3.0
        },
        {
            'username': 'Tester',
            'description': 'Filler Texfeaft',
             'rating': 5.0
        }
    ]
