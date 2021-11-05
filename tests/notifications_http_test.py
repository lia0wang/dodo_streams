import requests
import pytest

from src import config

BASE_URL = config.url

def test_http_channel_invite_basic():
    requests.delete(f"{BASE_URL}/clear/v1", json = {})

    register_param_1 = {
        "email": "11037.666@gmail.com",
        "password": "Hope11037",
        "name_first": "Hopeful",
        "name_last": "Boyyy"
    }
    user_1 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_1).json()

    channel_param = {
        'token': user_1['token'],
        'name': 'league',
        'is_public': True
    }
    channel = requests.post(f"{BASE_URL}/channels/create/v2", json = channel_param).json() 

    register_param_2 = {
        "email": "z5306312@gmail.com",
        "password": "LeonLiao123",
        "name_first": "Leon",
        "name_last": "Liao"
    }
    user_2 = requests.post(f"{BASE_URL}/auth/register/v2", json = register_param_2).json()
    
    channel_invites_param = {
        'token': user_1['token'],
        'channel_id': channel['channel_id'],
        'u_id': user_2['auth_user_id']
    }
    response = requests.post(f"{BASE_URL}/channel/invite/v2", json = channel_invites_param)
    assert response.status_code == 200

    token = {
        'token': user_2['token']
    }
    
    response = requests.get(f"{BASE_URL}/notifications/get/v1", params = token)
    assert response.status_code == 200
    notif = response.json()
    assert notif[0]['channel_id'] == 1
    assert notif[0]['dm_id'] == -1
    assert notif[0]['notification_message'] == 'added to a channel/DM: leonliao added you to league'