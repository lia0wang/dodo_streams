import pytest
import requests
from json import loads
from src.other import clear_v1

BASE_URL = 'http://localhost:8080'


def test_http_nonexistent_token():
    clear_v1()
    get_response = requests.get(f"{BASE_URL}/channels/list/v2", json = 389)
    assert get_response.status_code != 200

def test_http_valid_result():
    clear_v1()
    param0 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user = requests.post(f"{BASE_URL}/auth/register/v2", json = param0)
    user0 = loads(user.json())

    channel_param0 = {
        "token": user0['token'],
        "name": "test_channel1",
        "is_public": True
    }
    requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param0)

    get_response = requests.post(f"{BASE_URL}/channels/list/v2", json = user0['token'])
    assert get_response.status_code == 200