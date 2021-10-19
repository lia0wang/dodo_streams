from flask.wrappers import Response
import pytest
import requests
import pytest
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'

def test_http_channels_create_basic():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})
    
    register_param = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param).json()

    channel_param = {
        'token': user['token'],
        'name': 'league',
        'is_public': True
    }
    response = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param)

    assert response.status_code == 200

    channel = response.json()
    channel_id = channel['channel_id']
    assert channel_id == 1
