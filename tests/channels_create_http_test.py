from flask.wrappers import Response
import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

def test_gttp_channels_create_basic():
    clear_v1()
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()
    token = user['token']

    channel_param = {
        'token': token,
        'name': 'league',
        'is_public': True
    }
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)

    assert response == 200

    requested_data = response.json()
    channel_id = requested_data['channel_id']
    assert channel_id == 1
